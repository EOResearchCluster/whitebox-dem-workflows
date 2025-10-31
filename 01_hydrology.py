#!/usr/bin/env python3
"""
HYDROLOGY WORKFLOW
Comprehensive hydrological analysis using WhiteboxTools Python API

This script uses the whitebox Python package (open-source frontend to WhiteboxTools).

Usage:
    python 01_hydrology.py [DEM_FILE] [OUTPUT_DIR]
    python 01_hydrology.py dem.tif outputs/01_hydrology
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    import whitebox
except ImportError:
    print("ERROR: whitebox package not found.")
    print("Install with: pip install whitebox")
    print("Or use pixi: pixi install")
    sys.exit(1)


class HydrologyWorkflow:
    """Comprehensive hydrological analysis workflow"""

    def __init__(self, dem_file: str, output_dir: str, verbose: bool = True):
        self.dem_file = Path(dem_file).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.verbose = verbose

        # Initialize WhiteboxTools
        self.wbt = whitebox.WhiteboxTools()
        self.wbt.set_verbose_mode(verbose)
        self.wbt.set_max_procs(-1)  # Use all available cores
        self.wbt.set_compress_rasters(True)  # Compress output rasters

        # Check if DEM exists
        if not self.dem_file.exists():
            raise FileNotFoundError(f"DEM file not found: {self.dem_file}")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str, section: Optional[str] = None):
        """Print log message with timestamp"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            if section:
                print(f"[{timestamp}] [{section}] {message}")
            else:
                print(f"[{timestamp}] {message}")

    def run(self):
        """Execute complete hydrology workflow"""
        print("=" * 80)
        print("HYDROLOGY WORKFLOW STARTED")
        print(f"Input DEM: {self.dem_file}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 80)

        # Run workflow sections
        self.depression_handling()
        self.flow_direction()
        self.flow_accumulation()
        self.watershed_delineation()
        self.stream_metrics()
        self.flowpath_analysis()
        self.topographic_wetness()
        self.stream_power_indices()
        self.utility_analyses()

        print("\n" + "=" * 80)
        print("HYDROLOGY WORKFLOW COMPLETED")
        print(f"Outputs saved to: {self.output_dir}")
        print("=" * 80)

    def depression_handling(self):
        """Section 1: Depression handling"""
        self.log("Depression Handling...", "1/9")

        # Breach depressions (preferred method)
        self.log("  - Breaching depressions (Lindsay 2016 algorithm)...")
        self.wbt.breach_depressions(
            str(self.dem_file),
            str(self.output_dir / "dem_breached.tif")
        )

        # Breach depressions using least-cost method
        self.log("  - Breaching depressions (least-cost method)...")
        self.wbt.breach_depressions_least_cost(
            str(self.dem_file),
            str(self.output_dir / "dem_breached_leastcost.tif"),
            dist=1000
        )

        # Fill depressions (alternative method)
        self.log("  - Filling depressions...")
        self.wbt.fill_depressions(
            str(self.dem_file),
            str(self.output_dir / "dem_filled.tif")
        )

        # Fill single-cell pits
        self.log("  - Filling single-cell pits...")
        self.wbt.fill_single_cell_pits(
            str(self.dem_file),
            str(self.output_dir / "dem_pits_filled.tif")
        )

        # Depth in sink
        self.log("  - Calculating depth in sinks...")
        self.wbt.depth_in_sink(
            str(self.dem_file),
            str(self.output_dir / "depth_in_sink.tif")
        )

    def flow_direction(self):
        """Section 2: Flow direction analysis"""
        self.log("Flow Direction Analysis...", "2/9")

        dem_breached = str(self.output_dir / "dem_breached.tif")

        # D8 flow pointer
        self.log("  - D8 flow pointer...")
        self.wbt.d8_pointer(
            dem_breached,
            str(self.output_dir / "d8_pointer.tif")
        )

        # D-infinity flow pointer
        self.log("  - D-infinity flow pointer...")
        self.wbt.d_inf_pointer(
            dem_breached,
            str(self.output_dir / "dinf_pointer.tif")
        )

        # FD8 flow pointer
        self.log("  - FD8 flow pointer...")
        self.wbt.fd8_pointer(
            dem_breached,
            str(self.output_dir / "fd8_pointer.tif")
        )

    def flow_accumulation(self):
        """Section 3: Flow accumulation analysis"""
        self.log("Flow Accumulation Analysis...", "3/9")

        dem_breached = str(self.output_dir / "dem_breached.tif")

        # D8 flow accumulation
        self.log("  - D8 flow accumulation...")
        self.wbt.d8_flow_accumulation(
            dem_breached,
            str(self.output_dir / "d8_flow_accum.tif"),
            out_type="cells"
        )

        # D8 flow accumulation (specific catchment area)
        self.log("  - D8 flow accumulation (specific catchment area)...")
        self.wbt.d8_flow_accumulation(
            dem_breached,
            str(self.output_dir / "d8_flow_accum_sca.tif"),
            out_type="specific contributing area"
        )

        # D-infinity flow accumulation
        self.log("  - D-infinity flow accumulation...")
        self.wbt.d_inf_flow_accumulation(
            dem_breached,
            str(self.output_dir / "dinf_flow_accum.tif"),
            out_type="cells"
        )

        # D-infinity flow accumulation (specific catchment area)
        self.log("  - D-infinity flow accumulation (specific catchment area)...")
        self.wbt.d_inf_flow_accumulation(
            dem_breached,
            str(self.output_dir / "dinf_flow_accum_sca.tif"),
            out_type="specific contributing area"
        )

        # FD8 flow accumulation
        self.log("  - FD8 flow accumulation...")
        self.wbt.fd8_flow_accumulation(
            dem_breached,
            str(self.output_dir / "fd8_flow_accum.tif"),
            out_type="cells"
        )

    def watershed_delineation(self):
        """Section 4: Watershed delineation"""
        self.log("Watershed Delineation...", "4/9")

        d8_pointer = str(self.output_dir / "d8_pointer.tif")
        d8_accum = str(self.output_dir / "d8_flow_accum.tif")

        # Extract streams (needed for hillslopes and subbasins)
        self.log("  - Extracting streams for watershed analysis...")
        self.wbt.extract_streams(
            d8_accum,
            str(self.output_dir / "streams_temp.tif"),
            threshold=1000.0
        )

        streams = str(self.output_dir / "streams_temp.tif")

        # Drainage basins
        self.log("  - Extracting drainage basins...")
        self.wbt.basins(
            d8_pointer,
            str(self.output_dir / "basins.tif")
        )

        # Hillslopes (requires streams raster)
        self.log("  - Extracting hillslopes...")
        self.wbt.hillslopes(
            d8_pointer,
            streams,
            str(self.output_dir / "hillslopes.tif")
        )

        # Subbasins (requires streams raster)
        self.log("  - Extracting subbasins...")
        self.wbt.subbasins(
            d8_pointer,
            streams,
            str(self.output_dir / "subbasins.tif")
        )

    def stream_metrics(self):
        """Section 5: Stream-related metrics"""
        self.log("Stream-Related Metrics...", "5/9")

        dem_breached = str(self.output_dir / "dem_breached.tif")
        streams = str(self.output_dir / "streams_temp.tif")

        # Elevation above stream
        self.log("  - Calculating elevation above stream...")
        self.wbt.elevation_above_stream(
            dem_breached,
            streams,
            str(self.output_dir / "elevation_above_stream.tif")
        )

        # Downslope distance to stream
        self.log("  - Calculating downslope distance to stream...")
        self.wbt.downslope_distance_to_stream(
            dem_breached,
            streams,
            str(self.output_dir / "distance_to_stream.tif")
        )

    def flowpath_analysis(self):
        """Section 6: Flowpath analysis"""
        self.log("Flowpath Analysis...", "6/9")

        dem_breached = str(self.output_dir / "dem_breached.tif")
        d8_pointer = str(self.output_dir / "d8_pointer.tif")

        # Average upslope flowpath length
        self.log("  - Calculating average upslope flowpath length...")
        self.wbt.average_upslope_flowpath_length(
            d8_pointer,
            str(self.output_dir / "avg_upslope_flowpath_length.tif")
        )

        # Average flowpath slope
        self.log("  - Calculating average flowpath slope...")
        self.wbt.average_flowpath_slope(
            dem_breached,
            str(self.output_dir / "avg_flowpath_slope.tif")
        )

        # Downslope flowpath length
        self.log("  - Calculating downslope flowpath length...")
        self.wbt.downslope_flowpath_length(
            d8_pointer,
            str(self.output_dir / "downslope_flowpath_length.tif")
        )

        # Maximum upslope flowpath length
        self.log("  - Calculating maximum upslope flowpath length...")
        self.wbt.max_upslope_flowpath_length(
            d8_pointer,
            str(self.output_dir / "max_upslope_flowpath_length.tif")
        )

    def topographic_wetness(self):
        """Section 7: Topographic wetness indices"""
        self.log("Topographic Wetness Indices...", "7/9")

        # Check if slope from geomorphometry exists
        slope_path = Path("outputs/02_geomorphometry/slope_degrees.tif").resolve()
        if not slope_path.exists():
            self.log("    (Skipped - requires slope from geomorphometry)")
            return

        sca = str(self.output_dir / "d8_flow_accum_sca.tif")
        slope = str(slope_path)

        # Topographic wetness index (TWI)
        self.log("  - Calculating topographic wetness index (TWI)...")
        self.wbt.wetness_index(
            sca,
            slope,
            str(self.output_dir / "wetness_index.tif")
        )

    def stream_power_indices(self):
        """Section 8: Stream power and erosion indices"""
        self.log("Stream Power and Erosion Indices...", "8/9")

        # Check if slope from geomorphometry exists
        slope_path = Path("outputs/02_geomorphometry/slope_degrees.tif").resolve()
        if not slope_path.exists():
            self.log("    (Skipped - requires slope from geomorphometry)")
            return

        sca = str(self.output_dir / "d8_flow_accum_sca.tif")
        slope = str(slope_path)

        # Stream power index
        self.log("  - Calculating stream power index...")
        self.wbt.stream_power_index(
            sca,
            slope,
            str(self.output_dir / "stream_power_index.tif"),
            exponent=1.0
        )

        # Sediment transport index
        self.log("  - Calculating sediment transport index...")
        self.wbt.sediment_transport_index(
            sca,
            slope,
            str(self.output_dir / "sediment_transport_index.tif"),
            sca_exponent=1.0,
            slope_exponent=1.0
        )

    def utility_analyses(self):
        """Section 9: Utility analyses"""
        self.log("Utility Analyses...", "9/9")

        dem_breached = str(self.output_dir / "dem_breached.tif")
        d8_accum = str(self.output_dir / "d8_flow_accum.tif")

        # Find no-flow cells
        self.log("  - Finding no-flow cells...")
        self.wbt.find_no_flow_cells(
            dem_breached,
            str(self.output_dir / "no_flow_cells.tif")
        )

        # Edge contamination
        self.log("  - Detecting edge contamination...")
        self.wbt.edge_contamination(
            dem_breached,
            d8_accum,
            str(self.output_dir / "edge_contamination.tif")
        )

        # Elevation above pit
        self.log("  - Calculating elevation above pit...")
        self.wbt.elev_above_pit(
            dem_breached,
            str(self.output_dir / "elev_above_pit.tif")
        )


def main():
    parser = argparse.ArgumentParser(
        description="Hydrology Workflow - Comprehensive hydrological analysis using WhiteboxTools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "dem",
        nargs="?",
        default="dem.tif",
        help="Path to input DEM file (default: dem.tif)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="outputs/01_hydrology",
        help="Output directory (default: outputs/01_hydrology)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    try:
        workflow = HydrologyWorkflow(
            dem_file=args.dem,
            output_dir=args.output_dir,
            verbose=not args.quiet,
        )
        workflow.run()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
