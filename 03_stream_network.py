#!/usr/bin/env python3
"""
STREAM NETWORK ANALYSIS WORKFLOW
Comprehensive stream network analysis using WhiteboxTools Python API

This script uses the whitebox Python package (open-source frontend to WhiteboxTools).

Prerequisites: Requires outputs from 01_hydrology workflow

Usage:
    python 03_stream_network.py [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]
    python 03_stream_network.py dem.tif outputs/01_hydrology outputs/03_stream_network
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


class StreamNetworkWorkflow:
    """Comprehensive stream network analysis workflow"""

    def __init__(self, dem_file: str, hydro_dir: str, output_dir: str, verbose: bool = True):
        self.dem_file = Path(dem_file).resolve()
        self.hydro_dir = Path(hydro_dir).resolve()
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

        # Check if hydrology outputs exist
        if not (self.hydro_dir / "d8_pointer.tif").exists():
            raise FileNotFoundError(
                f"Hydrology workflow must be run first!\n"
                f"Run: python 01_hydrology.py {self.dem_file}"
            )

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
        """Execute complete stream network workflow"""
        print("=" * 80)
        print("STREAM NETWORK ANALYSIS STARTED")
        print(f"Input DEM: {self.dem_file}")
        print(f"Hydrology Directory: {self.hydro_dir}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 80)

        # Run workflow sections
        self.stream_extraction()
        self.stream_vectorization()
        self.stream_ordering()
        self.stream_link_analysis()
        self.tributary_analysis()
        self.channel_head_metrics()
        self.main_stem_identification()
        self.longitudinal_profiles()

        print("\n" + "=" * 80)
        print("STREAM NETWORK ANALYSIS COMPLETED")
        print(f"Outputs saved to: {self.output_dir}")
        print("=" * 80)

    def stream_extraction(self):
        """Section 1: Stream extraction"""
        self.log("Stream Extraction...", "1/8")

        d8_accum = str(self.hydro_dir / "d8_flow_accum.tif")
        dem_breached = str(self.hydro_dir / "dem_breached.tif")

        # Extract streams using different thresholds
        self.log("  - Extracting streams (threshold: 1000 cells)...")
        self.wbt.extract_streams(
            d8_accum,
            str(self.output_dir / "streams_1000.tif"),
            threshold=1000.0
        )

        self.log("  - Extracting streams (threshold: 500 cells)...")
        self.wbt.extract_streams(
            d8_accum,
            str(self.output_dir / "streams_500.tif"),
            threshold=500.0
        )

        self.log("  - Extracting streams (threshold: 2000 cells)...")
        self.wbt.extract_streams(
            d8_accum,
            str(self.output_dir / "streams_2000.tif"),
            threshold=2000.0
        )

        # Extract valleys
        self.log("  - Extracting valleys...")
        self.wbt.extract_valleys(
            dem_breached,
            str(self.output_dir / "valleys.tif")
        )

    def stream_vectorization(self):
        """Section 2: Stream vectorization"""
        self.log("Stream Vectorization...", "2/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")
        streams_500 = str(self.output_dir / "streams_500.tif")

        # Convert raster streams to vector
        self.log("  - Converting raster streams to vector (1000 threshold)...")
        self.wbt.raster_streams_to_vector(
            streams_1000,
            d8_pointer,
            str(self.output_dir / "streams_1000_vector.shp")
        )

        self.log("  - Converting raster streams to vector (500 threshold)...")
        self.wbt.raster_streams_to_vector(
            streams_500,
            d8_pointer,
            str(self.output_dir / "streams_500_vector.shp")
        )

    def stream_ordering(self):
        """Section 3: Stream ordering systems"""
        self.log("Stream Ordering Systems...", "3/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Strahler stream order
        self.log("  - Calculating Strahler stream order...")
        self.wbt.strahler_stream_order(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "strahler_order.tif")
        )

        # Horton stream order
        self.log("  - Calculating Horton stream order...")
        self.wbt.horton_stream_order(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "horton_order.tif")
        )

        # Shreve stream magnitude
        self.log("  - Calculating Shreve stream magnitude...")
        self.wbt.shreve_stream_magnitude(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "shreve_magnitude.tif")
        )

        # Hack stream order
        self.log("  - Calculating Hack stream order...")
        self.wbt.hack_stream_order(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "hack_order.tif")
        )

        # Topological stream order
        self.log("  - Calculating topological stream order...")
        self.wbt.topological_stream_order(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "topological_order.tif")
        )

    def stream_link_analysis(self):
        """Section 4: Stream link analysis"""
        self.log("Stream Link Analysis...", "4/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        dem_breached = str(self.hydro_dir / "dem_breached.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Stream link identifier
        self.log("  - Identifying stream links...")
        self.wbt.stream_link_identifier(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "stream_links.tif")
        )

        stream_links = str(self.output_dir / "stream_links.tif")

        # Stream link length
        self.log("  - Calculating stream link lengths...")
        self.wbt.stream_link_length(
            d8_pointer,
            stream_links,
            str(self.output_dir / "stream_link_length.tif")
        )

        # Stream link slope
        self.log("  - Calculating stream link slopes...")
        self.wbt.stream_link_slope(
            d8_pointer,
            stream_links,
            dem_breached,
            str(self.output_dir / "stream_link_slope.tif")
        )

        # Stream link class
        self.log("  - Classifying stream links...")
        self.wbt.stream_link_class(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "stream_link_class.tif")
        )

    def tributary_analysis(self):
        """Section 5: Tributary analysis"""
        self.log("Tributary Analysis...", "5/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Tributary identifier
        self.log("  - Identifying tributaries...")
        self.wbt.tributary_identifier(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "tributaries.tif")
        )

    def channel_head_metrics(self):
        """Section 6: Channel head and network metrics"""
        self.log("Channel Head and Network Metrics...", "6/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Farthest channel head
        self.log("  - Calculating distance to farthest channel head...")
        self.wbt.farthest_channel_head(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "farthest_channel_head.tif")
        )

        # Length of upstream channels
        self.log("  - Calculating length of upstream channels...")
        self.wbt.length_of_upstream_channels(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "upstream_channel_length.tif")
        )

        # Distance to outlet
        self.log("  - Calculating distance to outlet...")
        self.wbt.distance_to_outlet(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "distance_to_outlet.tif")
        )

    def main_stem_identification(self):
        """Section 7: Main stem identification"""
        self.log("Main Stem Identification...", "7/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Find main stem
        self.log("  - Finding main stem...")
        self.wbt.find_main_stem(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "main_stem.tif")
        )

    def longitudinal_profiles(self):
        """Section 8: Longitudinal profiles"""
        self.log("Longitudinal Profiles...", "8/8")

        d8_pointer = str(self.hydro_dir / "d8_pointer.tif")
        dem_breached = str(self.hydro_dir / "dem_breached.tif")
        streams_1000 = str(self.output_dir / "streams_1000.tif")

        # Long profile
        self.log("  - Creating longitudinal stream profile...")
        self.wbt.long_profile(
            d8_pointer,
            streams_1000,
            dem_breached,
            str(self.output_dir / "long_profile.html")
        )

        # Stream slope (continuous)
        self.log("  - Calculating continuous stream slope...")
        self.wbt.stream_slope_continuous(
            d8_pointer,
            streams_1000,
            dem_breached,
            str(self.output_dir / "stream_slope_continuous.tif")
        )

        # Remove short streams (creating cleaned network)
        self.log("  - Removing short streams (<100m)...")
        self.wbt.remove_short_streams(
            d8_pointer,
            streams_1000,
            str(self.output_dir / "streams_cleaned.tif"),
            min_length=100.0
        )


def main():
    parser = argparse.ArgumentParser(
        description="Stream Network Workflow - Comprehensive stream analysis using WhiteboxTools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "dem",
        nargs="?",
        default="dem.tif",
        help="Path to input DEM file (default: dem.tif)",
    )
    parser.add_argument(
        "hydro_dir",
        nargs="?",
        default="outputs/01_hydrology",
        help="Hydrology output directory (default: outputs/01_hydrology)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="outputs/03_stream_network",
        help="Output directory (default: outputs/03_stream_network)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    try:
        workflow = StreamNetworkWorkflow(
            dem_file=args.dem,
            hydro_dir=args.hydro_dir,
            output_dir=args.output_dir,
            verbose=not args.quiet,
        )
        workflow.run()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
