#!/usr/bin/env python3
"""
STREAM NETWORK ANALYSIS WORKFLOW
Comprehensive stream network analysis using WhiteboxTools
Usage: python 03_stream_network.py [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]
Prerequisites: Requires outputs from 01_hydrology.py
"""

import sys
from pathlib import Path
from whitebox_workflows import WbEnvironment


def print_step(step, total, message):
    """Print step progress"""
    print(f"\n[{step}/{total}] {message}...")


def stream_network_workflow(dem_file, hydro_dir, output_dir):
    """Run complete stream network analysis workflow"""

    # Check if DEM exists
    dem_path = Path(dem_file)
    if not dem_path.exists():
        print(f"ERROR: DEM file not found: {dem_file}")
        print(f"Usage: {sys.argv[0]} [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]")
        print(f"Example: {sys.argv[0]} mydem.tif outputs/01_hydrology outputs/03_stream_network")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 40)
    print("STREAM NETWORK ANALYSIS STARTED")
    print(f"Input DEM: {dem_file}")
    print(f"Hydrology Directory: {hydro_dir}")
    print(f"Output Directory: {output_dir}")
    print("=" * 40)

    # Check if hydrology outputs exist
    d8_pointer = Path(f"{hydro_dir}/d8_pointer.tif")
    if not d8_pointer.exists():
        print("ERROR: Hydrology workflow must be run first!")
        print("Run: python 01_hydrology.py")
        sys.exit(1)

    # Initialize WhiteboxTools environment
    wbe = WbEnvironment()

    # 1. STREAM EXTRACTION
    print_step(1, 8, "Stream Extraction")

    print("  - Extracting streams (threshold: 1000 cells)...")
    wbe.extract_streams(f"{hydro_dir}/d8_flow_accum.tif", f"{output_dir}/streams_1000.tif", threshold=1000)

    print("  - Extracting streams (threshold: 500 cells)...")
    wbe.extract_streams(f"{hydro_dir}/d8_flow_accum.tif", f"{output_dir}/streams_500.tif", threshold=500)

    print("  - Extracting streams (threshold: 2000 cells)...")
    wbe.extract_streams(f"{hydro_dir}/d8_flow_accum.tif", f"{output_dir}/streams_2000.tif", threshold=2000)

    print("  - Extracting valleys...")
    wbe.extract_valleys(f"{hydro_dir}/dem_breached.tif", f"{output_dir}/valleys.tif")

    # 2. STREAM VECTORIZATION
    print_step(2, 8, "Stream Vectorization")

    print("  - Converting raster streams to vector (1000 threshold)...")
    wbe.raster_streams_to_vector(f"{output_dir}/streams_1000.tif", f"{hydro_dir}/d8_pointer.tif",
                                 f"{output_dir}/streams_1000_vector.shp")

    print("  - Converting raster streams to vector (500 threshold)...")
    wbe.raster_streams_to_vector(f"{output_dir}/streams_500.tif", f"{hydro_dir}/d8_pointer.tif",
                                 f"{output_dir}/streams_500_vector.shp")

    # 3. STREAM ORDERING
    print_step(3, 8, "Stream Ordering Systems")

    print("  - Calculating Strahler stream order...")
    wbe.strahler_stream_order(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                             f"{output_dir}/strahler_order.tif")

    print("  - Calculating Horton stream order...")
    wbe.horton_stream_order(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                           f"{output_dir}/horton_order.tif")

    print("  - Calculating Shreve stream magnitude...")
    wbe.shreve_stream_magnitude(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                               f"{output_dir}/shreve_magnitude.tif")

    print("  - Calculating Hack stream order...")
    wbe.hack_stream_order(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                         f"{output_dir}/hack_order.tif")

    print("  - Calculating topological stream order...")
    wbe.topological_stream_order(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                                f"{output_dir}/topological_order.tif")

    # 4. STREAM LINK ANALYSIS
    print_step(4, 8, "Stream Link Analysis")

    print("  - Identifying stream links...")
    wbe.stream_link_identifier(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                              f"{output_dir}/stream_links.tif")

    print("  - Calculating stream link lengths...")
    wbe.stream_link_length(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/stream_links.tif",
                          f"{output_dir}/stream_link_length.tif")

    print("  - Calculating stream link slopes...")
    wbe.stream_link_slope(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/stream_links.tif",
                         f"{hydro_dir}/dem_breached.tif", f"{output_dir}/stream_link_slope.tif")

    print("  - Classifying stream links...")
    wbe.stream_link_class(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                         f"{output_dir}/stream_link_class.tif")

    # 5. TRIBUTARY ANALYSIS
    print_step(5, 8, "Tributary Analysis")

    print("  - Identifying tributaries...")
    wbe.tributary_identifier(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                            f"{output_dir}/tributaries.tif")

    # 6. CHANNEL HEAD AND NETWORK METRICS
    print_step(6, 8, "Channel Head and Network Metrics")

    print("  - Calculating distance to farthest channel head...")
    wbe.farthest_channel_head(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                             f"{output_dir}/farthest_channel_head.tif")

    print("  - Calculating length of upstream channels...")
    wbe.length_of_upstream_channels(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                                   f"{output_dir}/upstream_channel_length.tif")

    print("  - Calculating distance to outlet...")
    wbe.distance_to_outlet(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                          f"{output_dir}/distance_to_outlet.tif")

    # 7. MAIN STEM IDENTIFICATION
    print_step(7, 8, "Main Stem Identification")

    print("  - Finding main stem...")
    wbe.find_main_stem(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                      f"{output_dir}/main_stem.tif")

    # 8. LONGITUDINAL PROFILES
    print_step(8, 8, "Longitudinal Profiles")

    print("  - Creating longitudinal stream profile...")
    wbe.long_profile(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                    f"{hydro_dir}/dem_breached.tif", f"{output_dir}/long_profile.html")

    print("  - Calculating continuous stream slope...")
    wbe.stream_slope_continuous(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                               f"{hydro_dir}/dem_breached.tif", f"{output_dir}/stream_slope_continuous.tif")

    print("  - Removing short streams (<100m)...")
    wbe.remove_short_streams(f"{hydro_dir}/d8_pointer.tif", f"{output_dir}/streams_1000.tif",
                            f"{output_dir}/streams_cleaned.tif", min_length=100.0)

    print("\n" + "=" * 40)
    print("STREAM NETWORK ANALYSIS COMPLETED")
    print(f"Outputs saved to: {output_dir}")
    print("=" * 40)


def main():
    """Main entry point"""
    dem_file = sys.argv[1] if len(sys.argv) > 1 else "dem.tif"
    hydro_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/01_hydrology"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "outputs/03_stream_network"

    stream_network_workflow(dem_file, hydro_dir, output_dir)


if __name__ == "__main__":
    main()
