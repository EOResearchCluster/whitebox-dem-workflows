#!/usr/bin/env python3
"""
WhiteboxTools Geoprocessing Workflow Manager

This script provides a Python interface to run WhiteboxTools workflows
with options for parallel execution, selective workflow running, and
progress monitoring.

Usage:
    python run_workflows.py --all              # Run all workflows sequentially
    python run_workflows.py --parallel         # Run independent workflows in parallel
    python run_workflows.py --workflow hydrology  # Run specific workflow
    python run_workflows.py --list             # List available workflows
"""

import subprocess
import argparse
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


class WorkflowManager:
    """Manages execution of WhiteboxTools workflows"""

    def __init__(self, dem_file: str = "DEM5_bbox_Dettelbach.tif"):
        self.dem_file = Path(dem_file)
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        # Define workflows with their properties
        self.workflows = {
            'geomorphometry': {
                'script': '02_geomorphometry.sh',
                'name': 'Geomorphometry Analysis',
                'description': 'Terrain attributes, curvatures, roughness, and landforms',
                'dependencies': [],
                'output_dir': 'outputs/02_geomorphometry'
            },
            'hydrology': {
                'script': '01_hydrology.sh',
                'name': 'Hydrological Analysis',
                'description': 'Flow direction, accumulation, watersheds, and wetness indices',
                'dependencies': [],
                'output_dir': 'outputs/01_hydrology'
            },
            'stream_network': {
                'script': '03_stream_network.sh',
                'name': 'Stream Network Analysis',
                'description': 'Stream extraction, ordering, and longitudinal profiles',
                'dependencies': ['hydrology'],
                'output_dir': 'outputs/03_stream_network'
            },
            'morphometry': {
                'script': '04_morphometry.sh',
                'name': 'Morphometric Analysis',
                'description': 'Advanced terrain metrics, texture, and relative position',
                'dependencies': [],
                'output_dir': 'outputs/04_morphometry'
            }
        }

    def print_status(self, message: str, color: str = Colors.BLUE):
        """Print status message with timestamp and color"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{timestamp}]{Colors.NC} {message}")

    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met"""
        # Check if DEM exists
        if not self.dem_file.exists():
            self.print_error(f"DEM file not found: {self.dem_file}")
            return False

        # Check if whitebox_tools is available
        try:
            result = subprocess.run(
                ['whitebox_tools', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.print_success("WhiteboxTools found and accessible")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_error("WhiteboxTools not found. Install with: pixi global install whitebox_tools")
            return False

        return False

    def make_executable(self, script_path: str):
        """Make script executable"""
        os.chmod(script_path, 0o755)

    def run_workflow(self, workflow_key: str) -> Tuple[bool, float, str]:
        """
        Run a single workflow

        Returns:
            Tuple of (success, duration, log_file)
        """
        workflow = self.workflows[workflow_key]
        script = workflow['script']
        name = workflow['name']

        # Make script executable
        self.make_executable(script)

        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{workflow_key}_{timestamp}.log"

        self.print_status(f"Starting {name}...")
        start_time = time.time()

        try:
            with open(log_file, 'w') as log:
                process = subprocess.Popen(
                    ['bash', script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                # Stream output to console and log file
                for line in process.stdout:
                    print(line, end='')
                    log.write(line)

                process.wait()
                duration = time.time() - start_time

                if process.returncode == 0:
                    self.print_success(f"{name} completed in {duration:.1f} seconds")
                    return True, duration, str(log_file)
                else:
                    self.print_error(f"{name} failed with return code {process.returncode}")
                    return False, duration, str(log_file)

        except Exception as e:
            duration = time.time() - start_time
            self.print_error(f"{name} failed with exception: {e}")
            return False, duration, str(log_file)

    def run_sequential(self, workflow_keys: List[str]) -> Dict:
        """Run workflows sequentially"""
        results = {}
        total_start = time.time()

        for workflow_key in workflow_keys:
            success, duration, log_file = self.run_workflow(workflow_key)
            results[workflow_key] = {
                'success': success,
                'duration': duration,
                'log_file': log_file
            }

        total_duration = time.time() - total_start
        results['total_duration'] = total_duration

        return results

    def run_parallel(self) -> Dict:
        """Run independent workflows in parallel"""
        # Separate workflows into independent and dependent
        independent = ['geomorphometry', 'hydrology', 'morphometry']
        dependent = ['stream_network']

        results = {}
        total_start = time.time()

        # Run independent workflows in parallel
        self.print_status(f"Running {len(independent)} independent workflows in parallel...")

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.run_workflow, key): key
                for key in independent
            }

            for future in as_completed(futures):
                workflow_key = futures[future]
                success, duration, log_file = future.result()
                results[workflow_key] = {
                    'success': success,
                    'duration': duration,
                    'log_file': log_file
                }

        # Run dependent workflows if prerequisites succeeded
        if results.get('hydrology', {}).get('success', False):
            self.print_status("Running dependent workflows...")
            for workflow_key in dependent:
                success, duration, log_file = self.run_workflow(workflow_key)
                results[workflow_key] = {
                    'success': success,
                    'duration': duration,
                    'log_file': log_file
                }
        else:
            self.print_warning("Skipping stream network analysis (hydrology failed)")

        total_duration = time.time() - total_start
        results['total_duration'] = total_duration

        return results

    def list_workflows(self):
        """List all available workflows"""
        print(f"\n{Colors.BOLD}Available Workflows:{Colors.NC}\n")
        for key, workflow in self.workflows.items():
            deps = ', '.join(workflow['dependencies']) if workflow['dependencies'] else 'None'
            print(f"{Colors.CYAN}{key:20}{Colors.NC} - {workflow['name']}")
            print(f"{'':20}   {workflow['description']}")
            print(f"{'':20}   Dependencies: {deps}")
            print(f"{'':20}   Script: {workflow['script']}")
            print()

    def print_summary(self, results: Dict):
        """Print execution summary"""
        print("\n" + "=" * 80)
        print(f"{Colors.BOLD}EXECUTION SUMMARY{Colors.NC}")
        print("=" * 80 + "\n")

        successful = []
        failed = []

        for key, result in results.items():
            if key == 'total_duration':
                continue

            workflow = self.workflows[key]
            if result['success']:
                successful.append(key)
                status = f"{Colors.GREEN}✓ SUCCESS{Colors.NC}"
            else:
                failed.append(key)
                status = f"{Colors.RED}✗ FAILED{Colors.NC}"

            print(f"{status} {workflow['name']:30} ({result['duration']:.1f}s)")
            print(f"{'':10}Log: {result['log_file']}")

        print("\n" + "-" * 80)
        print(f"Total execution time: {results['total_duration']:.1f} seconds "
              f"({results['total_duration'] / 60:.1f} minutes)")
        print(f"Successful: {len(successful)}/{len(results)-1}")
        if failed:
            print(f"{Colors.RED}Failed: {', '.join(failed)}{Colors.NC}")

        # Count output files
        print("\n" + "-" * 80)
        print("Output file counts:")
        for key in self.workflows.keys():
            output_dir = Path(self.workflows[key]['output_dir'])
            if output_dir.exists():
                file_count = len(list(output_dir.rglob('*')))
                print(f"  {key:20} {file_count:4} files")

        print("\n" + "=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='WhiteboxTools Workflow Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_workflows.py --all              # Run all workflows sequentially
  python run_workflows.py --parallel         # Run independent workflows in parallel
  python run_workflows.py --workflow hydrology  # Run specific workflow
  python run_workflows.py --list             # List available workflows
        """
    )

    parser.add_argument('--all', action='store_true',
                        help='Run all workflows sequentially')
    parser.add_argument('--parallel', action='store_true',
                        help='Run independent workflows in parallel')
    parser.add_argument('--workflow', type=str, choices=['hydrology', 'geomorphometry',
                                                          'stream_network', 'morphometry'],
                        help='Run a specific workflow')
    parser.add_argument('--list', action='store_true',
                        help='List available workflows')
    parser.add_argument('--dem', type=str, default='DEM5_bbox_Dettelbach.tif',
                        help='Path to DEM file (default: DEM5_bbox_Dettelbach.tif)')

    args = parser.parse_args()

    # Create workflow manager
    manager = WorkflowManager(dem_file=args.dem)

    # List workflows
    if args.list:
        manager.list_workflows()
        return

    # Check prerequisites
    if not manager.check_prerequisites():
        sys.exit(1)

    # Print header
    print("\n" + "=" * 80)
    print(f"{Colors.BOLD}WHITEBOX GEOPROCESSING WORKFLOWS{Colors.NC}")
    print("=" * 80)
    print(f"Input DEM: {manager.dem_file}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # Run workflows based on arguments
    results = None

    if args.workflow:
        # Run specific workflow
        results = {}
        total_start = time.time()
        success, duration, log_file = manager.run_workflow(args.workflow)
        results[args.workflow] = {
            'success': success,
            'duration': duration,
            'log_file': log_file
        }
        results['total_duration'] = time.time() - total_start

    elif args.parallel:
        # Run in parallel
        results = manager.run_parallel()

    elif args.all:
        # Run all sequentially
        workflow_order = ['geomorphometry', 'hydrology', 'stream_network', 'morphometry']
        results = manager.run_sequential(workflow_order)

    else:
        parser.print_help()
        return

    # Print summary
    if results:
        manager.print_summary(results)


if __name__ == '__main__':
    main()
