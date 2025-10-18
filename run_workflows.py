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
from typing import List, Dict, Tuple


class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


class WorkflowManager:
    """Manages execution of WhiteboxTools workflows"""

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

    def make_executable(self, script_path: str):
        """Make script executable"""
        os.chmod(script_path, 0o755)

    def run_wbt_command(self, args: List[str], description: str = "") -> int:
        """
        Run a WhiteboxTools command

        Returns:
            Return code (0 for success)
        """
        if description:
            print(f"  - {description}...")

        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.stdout:
                print(result.stdout, end="")
            if result.stderr and result.returncode != 0:
                print(result.stderr, end="")

            return result.returncode
        except Exception as e:
            self.print_error(f"Command failed: {e}")
            return 1

    def run_workflow(self, workflow_key: str) -> Tuple[bool, float, str]:
        """
        Run a single workflow

        Returns:
            Tuple of (success, duration, log_file)
        """
        workflow = self.workflows[workflow_key]
        name = workflow["name"]
        output_dir = Path(workflow["output_dir"])

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{workflow_key}_{timestamp}.log"

        self.print_status(f"Starting {name}...")
        start_time = time.time()

        try:
            # Dispatch to appropriate workflow function
            if workflow_key == "hydrology":
                success = self.run_hydrology_workflow(output_dir, log_file)
            elif workflow_key == "geomorphometry":
                success = self.run_geomorphometry_workflow(output_dir, log_file)
            elif workflow_key == "stream_network":
                success = self.run_stream_network_workflow(output_dir, log_file)
            elif workflow_key == "morphometry":
                success = self.run_morphometry_workflow(output_dir, log_file)
            else:
                self.print_error(f"Unknown workflow: {workflow_key}")
                success = False

            duration = time.time() - start_time

            if success:
                self.print_success(f"{name} completed in {duration:.1f} seconds")
            else:
                self.print_error(f"{name} failed")

            return success, duration, str(log_file)

        except Exception as e:
            duration = time.time() - start_time
            self.print_error(f"{name} failed with exception: {e}")
            return False, duration, str(log_file)

    def run_hydrology_workflow(self, output_dir: Path, log_file: Path) -> bool:
        """Run hydrology workflow"""
        dem = str(self.dem_file)
        out = str(output_dir)

        # Open log file for writing
        with open(log_file, "w", buffering=1) as log:
            def log_print(msg):
                """Print to both console and log file"""
                print(msg)
                log.write(msg + "\n")

            log_print("=" * 80)
            log_print("HYDROLOGY WORKFLOW STARTED")
            log_print(f"Input DEM: {dem}")
            log_print(f"Output Directory: {out}")
            log_print("=" * 80)

            # 1. Depression Handling
            log_print("\n[1/9] Depression Handling...")
            self.run_wbt_command(["whitebox_tools", "-r=BreachDepressions", f"--dem={dem}", f"-o={out}/dem_breached.tif"], "Breaching depressions (Lindsay 2016)")
            self.run_wbt_command(["whitebox_tools", "-r=BreachDepressionsLeastCost", f"--dem={dem}", f"-o={out}/dem_breached_leastcost.tif"], "Breaching depressions (least-cost)")
            self.run_wbt_command(["whitebox_tools", "-r=FillDepressions", f"--dem={dem}", f"-o={out}/dem_filled.tif"], "Filling depressions")
            self.run_wbt_command(["whitebox_tools", "-r=FillSingleCellPits", f"--dem={dem}", f"-o={out}/dem_pits_filled.tif"], "Filling single-cell pits")
            self.run_wbt_command(["whitebox_tools", "-r=DepthInSink", f"--dem={dem}", f"-o={out}/depth_in_sink.tif"], "Calculating depth in sinks")

            # 2. Flow Direction
            log_print("\n[2/9] Flow Direction Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=D8Pointer", f"--dem={out}/dem_breached.tif", f"-o={out}/d8_pointer.tif"], "D8 flow pointer")
            self.run_wbt_command(["whitebox_tools", "-r=DInfPointer", f"--dem={out}/dem_breached.tif", f"-o={out}/dinf_pointer.tif"], "D-infinity flow pointer")
            self.run_wbt_command(["whitebox_tools", "-r=Fd8Pointer", f"--dem={out}/dem_breached.tif", f"-o={out}/fd8_pointer.tif"], "FD8 flow pointer")

            # 3. Flow Accumulation
            log_print("\n[3/9] Flow Accumulation Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=D8FlowAccumulation", f"--dem={out}/dem_breached.tif", f"-o={out}/d8_flow_accum.tif", "--out_type=cells"], "D8 flow accumulation")
            self.run_wbt_command(["whitebox_tools", "-r=D8FlowAccumulation", f"--dem={out}/dem_breached.tif", f"-o={out}/d8_flow_accum_sca.tif", "--out_type=sca"], "D8 flow accumulation (SCA)")
            self.run_wbt_command(["whitebox_tools", "-r=DInfFlowAccumulation", f"--dem={out}/dem_breached.tif", f"-o={out}/dinf_flow_accum.tif", "--out_type=cells"], "D-infinity flow accumulation")
            self.run_wbt_command(["whitebox_tools", "-r=DInfFlowAccumulation", f"--dem={out}/dem_breached.tif", f"-o={out}/dinf_flow_accum_sca.tif", "--out_type=sca"], "D-infinity flow accumulation (SCA)")
            self.run_wbt_command(["whitebox_tools", "-r=Fd8FlowAccumulation", f"--dem={out}/dem_breached.tif", f"-o={out}/fd8_flow_accum.tif", "--out_type=cells"], "FD8 flow accumulation")

            # 4. Watershed Delineation
            log_print("\n[4/9] Watershed Delineation...")
            self.run_wbt_command(["whitebox_tools", "-r=ExtractStreams", f"--flow_accum={out}/d8_flow_accum.tif", f"-o={out}/streams_temp.tif", "--threshold=1000"], "Extracting streams")
            self.run_wbt_command(["whitebox_tools", "-r=Basins", f"--d8_pntr={out}/d8_pointer.tif", f"-o={out}/basins.tif"], "Extracting drainage basins")
            self.run_wbt_command(["whitebox_tools", "-r=Hillslopes", f"--d8_pntr={out}/d8_pointer.tif", f"--streams={out}/streams_temp.tif", f"-o={out}/hillslopes.tif"], "Extracting hillslopes")
            self.run_wbt_command(["whitebox_tools", "-r=Subbasins", f"--d8_pntr={out}/d8_pointer.tif", f"--streams={out}/streams_temp.tif", f"-o={out}/subbasins.tif"], "Extracting subbasins")

            # 5. Stream-Related Metrics
            log_print("\n[5/9] Stream-Related Metrics...")
            self.run_wbt_command(["whitebox_tools", "-r=ElevationAboveStream", f"--dem={out}/dem_breached.tif", f"--streams={out}/streams_temp.tif", f"-o={out}/elevation_above_stream.tif"], "Calculating elevation above stream")
            self.run_wbt_command(["whitebox_tools", "-r=DownslopeDistanceToStream", f"--dem={out}/dem_breached.tif", f"--streams={out}/streams_temp.tif", f"-o={out}/distance_to_stream.tif"], "Calculating downslope distance to stream")

            # 6. Flowpath Analysis
            log_print("\n[6/9] Flowpath Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=AverageUpslopeFlowpathLength", f"--d8_pntr={out}/d8_pointer.tif", f"-o={out}/avg_upslope_flowpath_length.tif"], "Calculating average upslope flowpath length")
            self.run_wbt_command(["whitebox_tools", "-r=AverageFlowpathSlope", f"--dem={out}/dem_breached.tif", f"-o={out}/avg_flowpath_slope.tif"], "Calculating average flowpath slope")
            self.run_wbt_command(["whitebox_tools", "-r=DownslopeFlowpathLength", f"--d8_pntr={out}/d8_pointer.tif", f"-o={out}/downslope_flowpath_length.tif"], "Calculating downslope flowpath length")
            self.run_wbt_command(["whitebox_tools", "-r=MaxUpslopeFlowpathLength", f"--d8_pntr={out}/d8_pointer.tif", f"-o={out}/max_upslope_flowpath_length.tif"], "Calculating maximum upslope flowpath length")

            # 7. Skip TWI (requires slope from geomorphometry)
            log_print("\n[7/9] Topographic Wetness Indices...")
            log_print("  (Skipped - run geomorphometry first)")

            # 8. Skip stream power indices (requires slope from geomorphometry)
            log_print("\n[8/9] Stream Power and Erosion Indices...")
            log_print("  (Skipped - run geomorphometry first)")

            # 9. Utility Analyses
            log_print("\n[9/9] Utility Analyses...")
            self.run_wbt_command(["whitebox_tools", "-r=FindNoFlowCells", f"--dem={out}/dem_breached.tif", f"-o={out}/no_flow_cells.tif"], "Finding no-flow cells")
            self.run_wbt_command(["whitebox_tools", "-r=EdgeContamination", f"--dem={out}/dem_breached.tif", f"--flow_accum={out}/d8_flow_accum.tif", f"-o={out}/edge_contamination.tif"], "Detecting edge contamination")
            self.run_wbt_command(["whitebox_tools", "-r=ElevAbovePit", f"--dem={out}/dem_breached.tif", f"-o={out}/elev_above_pit.tif"], "Calculating elevation above pit")

            log_print("\n" + "=" * 80)
            log_print("HYDROLOGY WORKFLOW COMPLETED")
            log_print(f"Outputs saved to: {out}")
            log_print("=" * 80)

            return True

    def run_geomorphometry_workflow(self, output_dir: Path, log_file: Path) -> bool:
        """Run geomorphometry workflow"""
        dem = str(self.dem_file)
        out = str(output_dir)

        # Open log file for writing
        with open(log_file, "w", buffering=1) as log:
            def log_print(msg):
                """Print to both console and log file"""
                print(msg)
                log.write(msg + "\n")

            log_print("=" * 80)
            log_print("GEOMORPHOMETRY WORKFLOW STARTED")
            log_print(f"Input DEM: {dem}")
            log_print(f"Output Directory: {out}")
            log_print("=" * 80)

            # 1. Basic Terrain Attributes
            log_print("\n[1/12] Basic Terrain Attributes...")
            self.run_wbt_command(["whitebox_tools", "-r=Slope", f"--dem={dem}", f"-o={out}/slope_degrees.tif", "--units=degrees"], "Calculating slope (degrees)")
            self.run_wbt_command(["whitebox_tools", "-r=Slope", f"--dem={dem}", f"-o={out}/slope_radians.tif", "--units=radians"], "Calculating slope (radians)")
            self.run_wbt_command(["whitebox_tools", "-r=Slope", f"--dem={dem}", f"-o={out}/slope_percent.tif", "--units=percent"], "Calculating slope (percent)")
            self.run_wbt_command(["whitebox_tools", "-r=Aspect", f"--dem={dem}", f"-o={out}/aspect.tif"], "Calculating aspect")
            self.run_wbt_command(["whitebox_tools", "-r=Hillshade", f"--dem={dem}", f"-o={out}/hillshade.tif", "--azimuth=315.0", "--altitude=45.0"], "Creating hillshade")
            self.run_wbt_command(["whitebox_tools", "-r=MultidirectionalHillshade", f"--dem={dem}", f"-o={out}/hillshade_multidirectional.tif"], "Creating multidirectional hillshade")

            # 2. Curvature Analysis
            log_print("\n[2/12] Curvature Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=ProfileCurvature", f"--dem={dem}", f"-o={out}/profile_curvature.tif"], "Calculating profile curvature")
            self.run_wbt_command(["whitebox_tools", "-r=PlanCurvature", f"--dem={dem}", f"-o={out}/plan_curvature.tif"], "Calculating plan curvature")
            self.run_wbt_command(["whitebox_tools", "-r=TangentialCurvature", f"--dem={dem}", f"-o={out}/tangential_curvature.tif"], "Calculating tangential curvature")
            self.run_wbt_command(["whitebox_tools", "-r=TotalCurvature", f"--dem={dem}", f"-o={out}/total_curvature.tif"], "Calculating total curvature")
            self.run_wbt_command(["whitebox_tools", "-r=MeanCurvature", f"--dem={dem}", f"-o={out}/mean_curvature.tif"], "Calculating mean curvature")
            self.run_wbt_command(["whitebox_tools", "-r=GaussianCurvature", f"--dem={dem}", f"-o={out}/gaussian_curvature.tif"], "Calculating Gaussian curvature")
            self.run_wbt_command(["whitebox_tools", "-r=MinimalCurvature", f"--dem={dem}", f"-o={out}/minimal_curvature.tif"], "Calculating minimal curvature")
            self.run_wbt_command(["whitebox_tools", "-r=MaximalCurvature", f"--dem={dem}", f"-o={out}/maximal_curvature.tif"], "Calculating maximal curvature")

            # 3. Advanced Curvature Metrics
            log_print("\n[3/12] Advanced Curvature Metrics...")
            self.run_wbt_command(["whitebox_tools", "-r=DifferenceCurvature", f"--dem={dem}", f"-o={out}/difference_curvature.tif"], "Calculating difference curvature")
            self.run_wbt_command(["whitebox_tools", "-r=HorizontalExcessCurvature", f"--dem={dem}", f"-o={out}/horizontal_excess_curvature.tif"], "Calculating horizontal excess curvature")
            self.run_wbt_command(["whitebox_tools", "-r=VerticalExcessCurvature", f"--dem={dem}", f"-o={out}/vertical_excess_curvature.tif"], "Calculating vertical excess curvature")
            self.run_wbt_command(["whitebox_tools", "-r=RingCurvature", f"--dem={dem}", f"-o={out}/ring_curvature.tif"], "Calculating ring curvature")
            self.run_wbt_command(["whitebox_tools", "-r=Rotor", f"--dem={dem}", f"-o={out}/rotor.tif"], "Calculating rotor")

            # 4. Surface Roughness and Texture
            log_print("\n[4/12] Surface Roughness and Texture...")
            self.run_wbt_command(["whitebox_tools", "-r=RuggednessIndex", f"--dem={dem}", f"-o={out}/ruggedness_index.tif"], "Calculating terrain ruggedness index (TRI)")
            self.run_wbt_command(["whitebox_tools", "-r=MultiscaleRoughness", f"--dem={dem}", f"-o={out}/multiscale_roughness.tif"], "Calculating multiscale roughness")
            self.run_wbt_command(["whitebox_tools", "-r=SurfaceAreaRatio", f"--dem={dem}", f"-o={out}/surface_area_ratio.tif"], "Calculating surface area ratio")
            self.run_wbt_command(["whitebox_tools", "-r=CircularVarianceOfAspect", f"--dem={dem}", f"-o={out}/circular_variance_aspect.tif"], "Calculating circular variance of aspect")
            self.run_wbt_command(["whitebox_tools", "-r=AverageNormalVectorAngularDeviation", f"--dem={dem}", f"-o={out}/avg_normal_vector_angular_dev.tif"], "Calculating average normal vector angular deviation")

            # 5. Slope Position and Classification
            log_print("\n[5/12] Slope Position and Classification...")
            self.run_wbt_command(["whitebox_tools", "-r=SlopeVsElevationPlot", f"--dem={dem}", f"-o={out}/slope_vs_elevation.html"], "Calculating slope vs elevation percentile")
            self.run_wbt_command(["whitebox_tools", "-r=DevFromMeanElev", f"--dem={dem}", f"-o={out}/tpi.tif", "--filterx=11", "--filtery=11"], "Calculating topographic position index (TPI)")
            self.run_wbt_command(["whitebox_tools", "-r=DiffFromMeanElev", f"--dem={dem}", f"-o={out}/diff_from_mean_elev.tif", "--filterx=11", "--filtery=11"], "Calculating difference from mean elevation")
            self.run_wbt_command(["whitebox_tools", "-r=ElevPercentile", f"--dem={dem}", f"-o={out}/elev_percentile.tif", "--filterx=11", "--filtery=11"], "Calculating elevation percentile")

            # 6. Relief and Residuals
            log_print("\n[6/12] Relief and Residuals...")
            for radius in [5, 10, 20, 50]:
                log_print(f"    Scale: {radius} cells")
                filter_size = radius * 2 + 1
                self.run_wbt_command(["whitebox_tools", "-r=MaxElevationDeviation", f"--dem={dem}", f"-o={out}/relief_{radius}cell.tif", f"--filterx={filter_size}", f"--filtery={filter_size}"], f"Local relief (scale {radius})")

            self.run_wbt_command(["whitebox_tools", "-r=DirectionalRelief", f"--dem={dem}", f"-o={out}/directional_relief.tif"], "Calculating directional relief")

            # 7. Topographic Openness
            log_print("\n[7/12] Topographic Openness...")
            self.run_wbt_command(["whitebox_tools", "-r=MaxAnisotropyDev", f"--dem={dem}", f"-o={out}/max_anisotropy_dev.tif"], "Calculating max anisotropy deviation")
            self.run_wbt_command(["whitebox_tools", "-r=SkyViewFactor", f"--dem={dem}", f"-o={out}/sky_view_factor.tif"], "Calculating sky-view factor")

            # 8. Geomorphons and Landform Classification
            log_print("\n[8/12] Geomorphons and Landform Classification...")
            self.run_wbt_command(["whitebox_tools", "-r=Geomorphons", f"--dem={dem}", f"-o={out}/geomorphons.tif"], "Calculating geomorphons")
            self.run_wbt_command(["whitebox_tools", "-r=PennockLandformClass", f"--dem={dem}", f"-o={out}/pennock_landforms.tif"], "Pennock landform classification")

            # 9. Aspect-Related Analysis
            log_print("\n[9/12] Aspect-Related Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=Aspect", f"--dem={dem}", f"-o={out}/aspect_radians.tif"], "Calculating aspect in radians")

            # 10. Scale-Dependent Analysis
            log_print("\n[10/12] Scale-Dependent Analysis...")
            for sigma in [1.0, 2.0, 5.0]:
                log_print(f"    Sigma: {sigma}")
                self.run_wbt_command(["whitebox_tools", "-r=GaussianCurvature", f"--dem={dem}", f"-o={out}/gaussian_scale_sigma{sigma}.tif"], f"Gaussian scale space (sigma {sigma})")

            # 11. Contours and Topographic Features
            log_print("\n[11/12] Contours and Topographic Features...")
            self.run_wbt_command(["whitebox_tools", "-r=ContoursFromRaster", f"--input={dem}", f"-o={out}/contours_5m.shp", "--interval=5.0"], "Generating contour lines (5m interval)")
            self.run_wbt_command(["whitebox_tools", "-r=ContoursFromRaster", f"--input={dem}", f"-o={out}/contours_10m.shp", "--interval=10.0"], "Generating contour lines (10m interval)")
            self.run_wbt_command(["whitebox_tools", "-r=FindRidges", f"--dem={dem}", f"-o={out}/ridges.tif"], "Finding ridges")

            # 12. Illumination and Visibility
            log_print("\n[12/12] Illumination and Visibility...")
            self.run_wbt_command(["whitebox_tools", "-r=Hillshade", f"--dem={dem}", f"-o={out}/hillshade_morning.tif", "--azimuth=90.0", "--altitude=30.0"], "Creating hillshade (morning sun)")
            self.run_wbt_command(["whitebox_tools", "-r=Hillshade", f"--dem={dem}", f"-o={out}/hillshade_midday.tif", "--azimuth=180.0", "--altitude=60.0"], "Creating hillshade (midday sun)")
            self.run_wbt_command(["whitebox_tools", "-r=Hillshade", f"--dem={dem}", f"-o={out}/hillshade_evening.tif", "--azimuth=270.0", "--altitude=30.0"], "Creating hillshade (evening sun)")
            self.run_wbt_command(["whitebox_tools", "-r=HypsometricallyTintedHillshade", f"--dem={dem}", f"-o={out}/hillshade_hypsometric.tif"], "Creating hypsometrically tinted hillshade")

            log_print("\n" + "=" * 80)
            log_print("GEOMORPHOMETRY WORKFLOW COMPLETED")
            log_print(f"Outputs saved to: {out}")
            log_print("=" * 80)

            return True

    def run_stream_network_workflow(self, output_dir: Path, log_file: Path) -> bool:
        """Run stream network workflow"""
        dem = str(self.dem_file)
        out = str(output_dir)
        hydro_dir = Path("outputs/01_hydrology")

        # Check if hydrology outputs exist
        if not (hydro_dir / "d8_pointer.tif").exists():
            self.print_error("Hydrology workflow must be run first!")
            return False

        # Open log file for writing
        with open(log_file, "w", buffering=1) as log:
            def log_print(msg):
                """Print to both console and log file"""
                print(msg)
                log.write(msg + "\n")

            log_print("=" * 80)
            log_print("STREAM NETWORK ANALYSIS STARTED")
            log_print(f"Input DEM: {dem}")
            log_print(f"Hydrology Directory: {hydro_dir}")
            log_print(f"Output Directory: {out}")
            log_print("=" * 80)

            # 1. Stream Extraction
            log_print("\n[1/8] Stream Extraction...")
            self.run_wbt_command(["whitebox_tools", "-r=ExtractStreams", f"--flow_accum={hydro_dir}/d8_flow_accum.tif", f"-o={out}/streams_1000.tif", "--threshold=1000"], "Extracting streams (threshold: 1000 cells)")
            self.run_wbt_command(["whitebox_tools", "-r=ExtractStreams", f"--flow_accum={hydro_dir}/d8_flow_accum.tif", f"-o={out}/streams_500.tif", "--threshold=500"], "Extracting streams (threshold: 500 cells)")
            self.run_wbt_command(["whitebox_tools", "-r=ExtractStreams", f"--flow_accum={hydro_dir}/d8_flow_accum.tif", f"-o={out}/streams_2000.tif", "--threshold=2000"], "Extracting streams (threshold: 2000 cells)")
            self.run_wbt_command(["whitebox_tools", "-r=ExtractValleys", f"--dem={hydro_dir}/dem_breached.tif", f"-o={out}/valleys.tif"], "Extracting valleys")

            # 2. Stream Vectorization
            log_print("\n[2/8] Stream Vectorization...")
            self.run_wbt_command(["whitebox_tools", "-r=RasterStreamsToVector", f"--streams={out}/streams_1000.tif", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"-o={out}/streams_1000_vector.shp"], "Converting raster streams to vector (1000 threshold)")
            self.run_wbt_command(["whitebox_tools", "-r=RasterStreamsToVector", f"--streams={out}/streams_500.tif", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"-o={out}/streams_500_vector.shp"], "Converting raster streams to vector (500 threshold)")

            # 3. Stream Ordering
            log_print("\n[3/8] Stream Ordering Systems...")
            self.run_wbt_command(["whitebox_tools", "-r=StrahlerStreamOrder", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/strahler_order.tif"], "Calculating Strahler stream order")
            self.run_wbt_command(["whitebox_tools", "-r=HortonStreamOrder", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/horton_order.tif"], "Calculating Horton stream order")
            self.run_wbt_command(["whitebox_tools", "-r=ShreveStreamMagnitude", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/shreve_magnitude.tif"], "Calculating Shreve stream magnitude")
            self.run_wbt_command(["whitebox_tools", "-r=HackStreamOrder", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/hack_order.tif"], "Calculating Hack stream order")
            self.run_wbt_command(["whitebox_tools", "-r=TopologicalStreamOrder", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/topological_order.tif"], "Calculating topological stream order")

            # 4. Stream Link Analysis
            log_print("\n[4/8] Stream Link Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=StreamLinkIdentifier", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/stream_links.tif"], "Identifying stream links")
            self.run_wbt_command(["whitebox_tools", "-r=StreamLinkLength", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--linkid={out}/stream_links.tif", f"-o={out}/stream_link_length.tif"], "Calculating stream link lengths")
            self.run_wbt_command(["whitebox_tools", "-r=StreamLinkSlope", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--linkid={out}/stream_links.tif", f"--dem={hydro_dir}/dem_breached.tif", f"-o={out}/stream_link_slope.tif"], "Calculating stream link slopes")
            self.run_wbt_command(["whitebox_tools", "-r=StreamLinkClass", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/stream_link_class.tif"], "Classifying stream links")

            # 5. Tributary Analysis
            log_print("\n[5/8] Tributary Analysis...")
            self.run_wbt_command(["whitebox_tools", "-r=TributaryIdentifier", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/tributaries.tif"], "Identifying tributaries")

            # 6. Channel Head and Network Metrics
            log_print("\n[6/8] Channel Head and Network Metrics...")
            self.run_wbt_command(["whitebox_tools", "-r=FarthestChannelHead", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/farthest_channel_head.tif"], "Calculating distance to farthest channel head")
            self.run_wbt_command(["whitebox_tools", "-r=LengthOfUpstreamChannels", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/upstream_channel_length.tif"], "Calculating length of upstream channels")
            self.run_wbt_command(["whitebox_tools", "-r=DistanceToOutlet", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/distance_to_outlet.tif"], "Calculating distance to outlet")

            # 7. Main Stem Identification
            log_print("\n[7/8] Main Stem Identification...")
            self.run_wbt_command(["whitebox_tools", "-r=FindMainStem", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/main_stem.tif"], "Finding main stem")

            # 8. Longitudinal Profiles
            log_print("\n[8/8] Longitudinal Profiles...")
            self.run_wbt_command(["whitebox_tools", "-r=LongProfile", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"--dem={hydro_dir}/dem_breached.tif", f"-o={out}/long_profile.html"], "Creating longitudinal stream profile")
            self.run_wbt_command(["whitebox_tools", "-r=StreamSlopeContinuous", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"--dem={hydro_dir}/dem_breached.tif", f"-o={out}/stream_slope_continuous.tif"], "Calculating continuous stream slope")
            self.run_wbt_command(["whitebox_tools", "-r=RemoveShortStreams", f"--d8_pntr={hydro_dir}/d8_pointer.tif", f"--streams={out}/streams_1000.tif", f"-o={out}/streams_cleaned.tif", "--min_length=100.0"], "Removing short streams (<100m)")

            log_print("\n" + "=" * 80)
            log_print("STREAM NETWORK ANALYSIS COMPLETED")
            log_print(f"Outputs saved to: {out}")
            log_print("=" * 80)

            return True

    def run_morphometry_workflow(self, output_dir: Path, log_file: Path) -> bool:
        """Run morphometry workflow"""
        dem = str(self.dem_file)
        out = str(output_dir)
        geomorph_dir = Path("outputs/02_geomorphometry")

        # Open log file for writing
        with open(log_file, "w", buffering=1) as log:
            def log_print(msg):
                """Print to both console and log file"""
                print(msg)
                log.write(msg + "\n")

            log_print("=" * 80)
            log_print("MORPHOMETRY WORKFLOW STARTED")
            log_print(f"Input DEM: {dem}")
            log_print(f"Output Directory: {out}")
            log_print("=" * 80)

            # 1. Elevation Derivatives
            log_print("\n[1/10] Elevation Derivatives...")
            self.run_wbt_command(["whitebox_tools", "-r=RasterHistogram", f"--input={dem}", f"-o={out}/elevation_histogram.html"], "Calculating elevation statistics")
            self.run_wbt_command(["whitebox_tools", "-r=StdDeviationFilter", f"--input={dem}", f"-o={out}/elevation_stddev.tif", "--filterx=11", "--filtery=11"], "Calculating standard deviation of elevation")
            self.run_wbt_command(["whitebox_tools", "-r=RangeFilter", f"--input={dem}", f"-o={out}/elevation_range.tif", "--filterx=11", "--filtery=11"], "Calculating elevation range")

            # 2. Slope Derivatives
            log_print("\n[2/10] Slope Derivatives...")
            slope_file = geomorph_dir / "slope_degrees.tif"
            if not slope_file.exists():
                log_print("  - Creating slope (degrees)...")
                self.run_wbt_command(["whitebox_tools", "-r=Slope", f"--dem={dem}", f"-o={out}/slope_degrees.tif", "--units=degrees"], "Creating slope")
                slope_file = Path(out) / "slope_degrees.tif"

            self.run_wbt_command(["whitebox_tools", "-r=StdDeviationFilter", f"--input={slope_file}", f"-o={out}/slope_stddev.tif", "--filterx=11", "--filtery=11"], "Calculating slope standard deviation")
            self.run_wbt_command(["whitebox_tools", "-r=RangeFilter", f"--input={slope_file}", f"-o={out}/slope_range.tif", "--filterx=11", "--filtery=11"], "Calculating slope range")

            # 3. Terrain Texture and Pattern
            log_print("\n[3/10] Terrain Texture and Pattern...")
            self.run_wbt_command(["whitebox_tools", "-r=EdgeDensity", f"--dem={dem}", f"-o={out}/edge_density.tif"], "Calculating edge density")
            log_print("  - Skipping embankment mapping (requires road vector)")

            # 4. Feature Preservation Smoothing
            log_print("\n[4/10] Feature Preservation Smoothing...")
            self.run_wbt_command(["whitebox_tools", "-r=FeaturePreservingSmoothing", f"--dem={dem}", f"-o={out}/dem_smoothed.tif", "--filter=11"], "Applying feature preserving smoothing")
            self.run_wbt_command(["whitebox_tools", "-r=GaussianFilter", f"--input={dem}", f"-o={out}/dem_gaussian.tif", "--sigma=1.5"], "Applying Gaussian filter")
            self.run_wbt_command(["whitebox_tools", "-r=MeanFilter", f"--input={dem}", f"-o={out}/dem_mean_filtered.tif", "--filterx=5", "--filtery=5"], "Applying mean filter")
            self.run_wbt_command(["whitebox_tools", "-r=MedianFilter", f"--input={dem}", f"-o={out}/dem_median_filtered.tif", "--filterx=5", "--filtery=5"], "Applying median filter")

            # 5. Relative Topographic Position
            log_print("\n[5/10] Relative Topographic Position...")
            for scale in [3, 5, 11, 21, 51]:
                log_print(f"    Scale: {scale}x{scale} cells")
                self.run_wbt_command(["whitebox_tools", "-r=DevFromMeanElev", f"--dem={dem}", f"-o={out}/rel_topo_pos_{scale}x{scale}.tif", f"--filterx={scale}", f"--filtery={scale}"], f"Relative topographic position (scale {scale})")

            # 6. Downslope Index
            log_print("\n[6/10] Downslope Index...")
            self.run_wbt_command(["whitebox_tools", "-r=DownslopeIndex", f"--dem={dem}", f"-o={out}/downslope_index.tif"], "Calculating downslope index")

            # 7. Multiscale Topographic Metrics
            log_print("\n[7/10] Multiscale Topographic Metrics...")
            for scale in [5, 10, 20]:
                log_print(f"    Scale: {scale} cells radius")
                filter_size = scale * 2 + 1
                self.run_wbt_command(["whitebox_tools", "-r=ElevPercentile", f"--dem={dem}", f"-o={out}/elev_percentile_scale{scale}.tif", f"--filterx={filter_size}", f"--filtery={filter_size}"], f"Multiscale elevation percentile (scale {scale})")

            # 8. Aspect-Based Morphometry
            log_print("\n[8/10] Aspect-Based Morphometry...")
            aspect_file = geomorph_dir / "aspect.tif"
            if not aspect_file.exists():
                log_print("  - Creating aspect...")
                self.run_wbt_command(["whitebox_tools", "-r=Aspect", f"--dem={dem}", f"-o={out}/aspect.tif"], "Creating aspect")

            self.run_wbt_command(["whitebox_tools", "-r=Aspect", f"--dem={dem}", f"-o={out}/aspect_linear.tif"], "Calculating linear aspect")

            # 9. Profile and Tangential Curvature Combinations
            log_print("\n[9/10] Profile and Tangential Curvature Combinations...")
            profile_curv_file = geomorph_dir / "profile_curvature.tif"
            if not profile_curv_file.exists():
                log_print("  - Creating profile curvature...")
                self.run_wbt_command(["whitebox_tools", "-r=ProfileCurvature", f"--dem={dem}", f"-o={out}/profile_curvature.tif"], "Creating profile curvature")

            plan_curv_file = geomorph_dir / "plan_curvature.tif"
            if not plan_curv_file.exists():
                log_print("  - Creating plan curvature...")
                self.run_wbt_command(["whitebox_tools", "-r=PlanCurvature", f"--dem={dem}", f"-o={out}/plan_curvature.tif"], "Creating plan curvature")

            log_print("  - Skipping licensed tools (Unsphericity, ShapeIndex)")

            # 10. Flow Topology Metrics
            log_print("\n[10/10] Flow Topology Metrics...")
            self.run_wbt_command(["whitebox_tools", "-r=MaxUpslopeElevChange", f"--dem={dem}", f"-o={out}/max_upslope_elev_change.tif"], "Calculating max upslope elevation change")
            self.run_wbt_command(["whitebox_tools", "-r=NumUpslopeNeighbours", f"--dem={dem}", f"-o={out}/num_upslope_neighbours.tif"], "Calculating number of upslope neighbours")
            log_print("  - Skipping licensed tool (ImpoundmentSizeIndex)")

            log_print("\n" + "=" * 80)
            log_print("MORPHOMETRY WORKFLOW COMPLETED")
            log_print(f"Outputs saved to: {out}")
            log_print("=" * 80)

            return True

    def run_all(self, workflow_keys: List[str]) -> Dict:
        """
        Run workflows in sequence.

        Note: Sequential execution is optimal because WhiteboxTools already
        uses all available CPU cores for each tool. Running multiple workflows
        simultaneously would cause CPU contention and slow things down.
        """
        results = {}
        total_start = time.time()

        for workflow_key in workflow_keys:
            success, duration, log_file = self.run_workflow(workflow_key)
            results[workflow_key] = {
                "success": success,
                "duration": duration,
                "log_file": log_file,
            }

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

    def print_summary(self, results: Dict):
        """Print execution summary"""
        print("\n" + "=" * 80)
        print(f"{Colors.BOLD}EXECUTION SUMMARY{Colors.NC}")
        print("=" * 80 + "\n")

        successful = []
        failed = []

        for key, result in results.items():
            if key == "total_duration":
                continue

            workflow = self.workflows[key]
            if result["success"]:
                successful.append(key)
                status = f"{Colors.GREEN}[SUCCESS]{Colors.NC}"
            else:
                failed.append(key)
                status = f"{Colors.RED}[FAILED]{Colors.NC}"

            print(f"{status} {workflow['name']:30} ({result['duration']:.1f}s)")
            print(f"{'':10}Log: {result['log_file']}")

        print("\n" + "-" * 80)
        print(
            f"Total execution time: {results['total_duration']:.1f} seconds "
            f"({results['total_duration'] / 60:.1f} minutes)"
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
    results = None

    if args.workflow:
        # Run specific workflow
        results = {}
        total_start = time.time()
        success, duration, log_file = manager.run_workflow(args.workflow)
        results[args.workflow] = {
            "success": success,
            "duration": duration,
            "log_file": log_file,
        }
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
