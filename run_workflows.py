#!/usr/bin/env python3
"""
WhiteboxTools Geoprocessing Workflow Manager

This script provides a Python interface to run WhiteboxTools workflows
with options for selective workflow running and progress monitoring.

Note: WhiteboxTools automatically uses all available CPU cores for each tool,
so running workflows sequentially is actually faster than trying to run
multiple workflows simultaneously (which would cause CPU contention).

Usage:
    python run_workflows.py --all              # Run all workflows
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
from typing import Final, TypedDict


class WorkflowConfig(TypedDict):
    """Type definition for workflow configuration"""

    script: str
    name: str
    description: str
    dependencies: list[str]
    output_dir: str


class WorkflowResult(TypedDict):
    """Type definition for workflow execution result"""

    success: bool
    duration: float
    log_file: str


class Colors:
    """ANSI color codes for terminal output"""

    RED: Final[str] = "\033[0;31m"
    GREEN: Final[str] = "\033[0;32m"
    YELLOW: Final[str] = "\033[1;33m"
    BLUE: Final[str] = "\033[0;34m"
    MAGENTA: Final[str] = "\033[0;35m"
    CYAN: Final[str] = "\033[0;36m"
    BOLD: Final[str] = "\033[1m"
    NC: Final[str] = "\033[0m"  # No Color


class WorkflowManager:
    """Manages execution of WhiteboxTools workflows"""

    dem_file: Path
    log_dir: Path
    workflows: dict[str, WorkflowConfig]

    def __init__(self, dem_file: str = "dem.tif"):
        self.dem_file = Path(dem_file)
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        # Define workflows with their properties
        self.workflows = {
            "geomorphometry": {
                "script": "02_geomorphometry.sh",
                "name": "Geomorphometry Analysis",
                "description": "Terrain attributes, curvatures, roughness, and landforms",
                "dependencies": [],
                "output_dir": "outputs/02_geomorphometry",
            },
            "hydrology": {
                "script": "01_hydrology.sh",
                "name": "Hydrological Analysis",
                "description": "Flow direction, accumulation, watersheds, and wetness indices",
                "dependencies": [],
                "output_dir": "outputs/01_hydrology",
            },
            "stream_network": {
                "script": "03_stream_network.sh",
                "name": "Stream Network Analysis",
                "description": "Stream extraction, ordering, and longitudinal profiles",
                "dependencies": ["hydrology"],
                "output_dir": "outputs/03_stream_network",
            },
            "morphometry": {
                "script": "04_morphometry.sh",
                "name": "Morphometric Analysis",
                "description": "Advanced terrain metrics, texture, and relative position",
                "dependencies": [],
                "output_dir": "outputs/04_morphometry",
            },
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
                ["whitebox_tools", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                self.print_success("WhiteboxTools found and accessible")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_error(
                "WhiteboxTools not found. Install with: pixi global install whitebox_tools"
            )
            return False

        return False

    def make_executable(self, script_path: str) -> None:
        """Make script executable"""
        _ = os.chmod(script_path, 0o755)

    def run_workflow(self, workflow_key: str) -> tuple[bool, float, str]:
        """
        Run a single workflow

        Returns:
            Tuple of (success, duration, log_file)
        """
        workflow = self.workflows[workflow_key]
        script = workflow["script"]
        name = workflow["name"]

        # Make script executable
        self.make_executable(script)

        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{workflow_key}_{timestamp}.log"

        self.print_status(f"Starting {name}...")
        start_time = time.time()

        try:
            with open(log_file, "w") as log:
                # Build command with DEM file and output directory arguments
                cmd = ["bash", script, str(self.dem_file), workflow["output_dir"]]

                # For morphometry workflow, also pass geomorphometry directory
                if workflow_key == "morphometry":
                    cmd.append("outputs/02_geomorphometry")

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )

                # Stream output to console and log file
                for line in process.stdout:
                    print(line, end="")
                    log.write(line)

                process.wait()
                duration = time.time() - start_time

                if process.returncode == 0:
                    self.print_success(f"{name} completed in {duration:.1f} seconds")
                    return True, duration, str(log_file)
                else:
                    self.print_error(
                        f"{name} failed with return code {process.returncode}"
                    )
                    return False, duration, str(log_file)

        except Exception as e:
            duration = time.time() - start_time
            self.print_error(f"{name} failed with exception: {e}")
            return False, duration, str(log_file)

    def run_all(self, workflow_keys: list[str]) -> dict[str, WorkflowResult | float]:
        """
        Run workflows in sequence.

        Note: Sequential execution is optimal because WhiteboxTools already
        uses all available CPU cores for each tool. Running multiple workflows
        simultaneously would cause CPU contention and slow things down.
        """
        results: dict[str, WorkflowResult | float] = {}
        total_start = time.time()

        for workflow_key in workflow_keys:
            success, duration, log_file = self.run_workflow(workflow_key)
            results[workflow_key] = WorkflowResult(
                success=success,
                duration=duration,
                log_file=log_file,
            )

            # Skip stream_network if hydrology failed
            if workflow_key == "hydrology" and not success:
                self.print_warning(
                    "Skipping stream network analysis (hydrology failed)"
                )
                if "stream_network" in workflow_keys:
                    workflow_keys.remove("stream_network")

        total_duration = time.time() - total_start
        results["total_duration"] = total_duration

        return results

    def list_workflows(self):
        """List all available workflows"""
        print(f"\n{Colors.BOLD}Available Workflows:{Colors.NC}\n")
        for key, workflow in self.workflows.items():
            deps = (
                ", ".join(workflow["dependencies"])
                if workflow["dependencies"]
                else "None"
            )
            print(f"{Colors.CYAN}{key:20}{Colors.NC} - {workflow['name']}")
            print(f"{'':20}   {workflow['description']}")
            print(f"{'':20}   Dependencies: {deps}")
            print(f"{'':20}   Script: {workflow['script']}")
            print()

    def print_summary(self, results: dict[str, WorkflowResult | float]) -> None:
        """Print execution summary"""
        print("\n" + "=" * 80)
        print(f"{Colors.BOLD}EXECUTION SUMMARY{Colors.NC}")
        print("=" * 80 + "\n")

        successful: list[str] = []
        failed: list[str] = []

        for key, result in results.items():
            if key == "total_duration":
                continue

            # Type guard: at this point we know result is WorkflowResult
            if isinstance(result, dict):
                workflow = self.workflows[key]
                if result["success"]:
                    successful.append(key)
                    status = f"{Colors.GREEN}✓ SUCCESS{Colors.NC}"
                else:
                    failed.append(key)
                    status = f"{Colors.RED}✗ FAILED{Colors.NC}"

                print(f"{status} {workflow['name']:30} ({result['duration']:.1f}s)")
                print(f"{'':10}Log: {result['log_file']}")

        print("\n" + "-" * 80)
        total_duration = results.get("total_duration", 0.0)
        if isinstance(total_duration, float):
            print(
                f"Total execution time: {total_duration:.1f} seconds "
                f"({total_duration / 60:.1f} minutes)"
            )
        print(f"Successful: {len(successful)}/{len(results) - 1}")
        if failed:
            print(f"{Colors.RED}Failed: {', '.join(failed)}{Colors.NC}")

        # Count output files
        print("\n" + "-" * 80)
        print("Output file counts:")
        for key in self.workflows.keys():
            output_dir = Path(self.workflows[key]["output_dir"])
            if output_dir.exists():
                file_count = len(list(output_dir.rglob("*")))
                print(f"  {key:20} {file_count:4} files")

        print("\n" + "=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="WhiteboxTools Workflow Manager - Note: WhiteboxTools automatically uses all CPU cores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_workflows.py --all              # Run all workflows
  python run_workflows.py --workflow hydrology  # Run specific workflow
  python run_workflows.py --list             # List available workflows

Note:
  WhiteboxTools automatically parallelizes each tool across all available CPU cores.
  Sequential workflow execution is optimal - running multiple workflows simultaneously
  would cause CPU contention and actually slow down processing.
        """,
    )

    parser.add_argument("--all", action="store_true", help="Run all workflows")
    parser.add_argument(
        "--workflow",
        type=str,
        choices=["hydrology", "geomorphometry", "stream_network", "morphometry"],
        help="Run a specific workflow",
    )
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument(
        "--dem",
        type=str,
        default="dem.tif",
        help="Path to DEM file (default: dem.tif)",
    )

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
    results: dict[str, WorkflowResult | float] | None = None

    if args.workflow:
        # Run specific workflow
        results = {}
        total_start = time.time()
        success, duration, log_file = manager.run_workflow(args.workflow)
        results[args.workflow] = WorkflowResult(
            success=success,
            duration=duration,
            log_file=log_file,
        )
        results["total_duration"] = time.time() - total_start

    elif args.all:
        # Run all workflows
        workflow_order = [
            "geomorphometry",
            "hydrology",
            "stream_network",
            "morphometry",
        ]
        results = manager.run_all(workflow_order)

    else:
        parser.print_help()
        return

    # Print summary
    if results:
        manager.print_summary(results)


if __name__ == "__main__":
    main()
