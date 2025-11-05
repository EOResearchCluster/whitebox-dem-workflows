#!/usr/bin/env python3
"""
HYDROLOGY WORKFLOW
Comprehensive hydrological analysis using WhiteboxTools
Usage: python 01_hydrology.py [DEM_FILE] [OUTPUT_DIR]
"""

import sys
from pathlib import Path
from whitebox_workflows import WbEnvironment


def print_step(step, total, message):
    """Print step progress"""
    print(f"\n[{step}/{total}] {message}...")


def hydrology_workflow(dem_file, output_dir):
    """Run complete hydrology workflow"""

    # Check if DEM exists
    dem_path = Path(dem_file)
    if not dem_path.exists():
        print(f"ERROR: DEM file not found: {dem_file}")
        print(f"Usage: {sys.argv[0]} [DEM_FILE] [OUTPUT_DIR]")
        print(f"Example: {sys.argv[0]} mydem.tif outputs/01_hydrology")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 40)
    print("HYDROLOGY WORKFLOW STARTED")
    print(f"Input DEM: {dem_file}")
    print(f"Output Directory: {output_dir}")
    print("=" * 40)

    # Initialize WhiteboxTools environment
    wbe = WbEnvironment()

    # ========================================================================
    # 1. DEPRESSION HANDLING
    # ========================================================================
    print_step(1, 9, "Depression Handling")

    # Breach depressions (preferred method)
    print("  - Breaching depressions (Lindsay 2016 algorithm)...")
    wbe.breach_depressions(dem_file, f"{output_dir}/dem_breached.tif")

    # Breach depressions using least-cost method
    print("  - Breaching depressions (least-cost method)...")
    wbe.breach_depressions_least_cost(dem_file, f"{output_dir}/dem_breached_leastcost.tif")

    # Fill depressions (alternative method)
    print("  - Filling depressions...")
    wbe.fill_depressions(dem_file, f"{output_dir}/dem_filled.tif")

    # Fill single-cell pits
    print("  - Filling single-cell pits...")
    wbe.fill_single_cell_pits(dem_file, f"{output_dir}/dem_pits_filled.tif")

    # Depth in sink
    print("  - Calculating depth in sinks...")
    wbe.depth_in_sink(dem_file, f"{output_dir}/depth_in_sink.tif")

    # ========================================================================
    # 2. FLOW DIRECTION (Using breached DEM)
    # ========================================================================
    print_step(2, 9, "Flow Direction Analysis")

    # D8 flow pointer
    print("  - D8 flow pointer...")
    wbe.d8_pointer(f"{output_dir}/dem_breached.tif", f"{output_dir}/d8_pointer.tif")

    # D-infinity flow pointer
    print("  - D-infinity flow pointer...")
    wbe.d_inf_pointer(f"{output_dir}/dem_breached.tif", f"{output_dir}/dinf_pointer.tif")

    # FD8 flow pointer
    print("  - FD8 flow pointer...")
    wbe.fd8_pointer(f"{output_dir}/dem_breached.tif", f"{output_dir}/fd8_pointer.tif")

    # ========================================================================
    # 3. FLOW ACCUMULATION
    # ========================================================================
    print_step(3, 9, "Flow Accumulation Analysis")

    # D8 flow accumulation
    print("  - D8 flow accumulation...")
    wbe.d8_flow_accumulation(f"{output_dir}/dem_breached.tif", f"{output_dir}/d8_flow_accum.tif", out_type="cells")

    # D8 flow accumulation (specific catchment area)
    print("  - D8 flow accumulation (specific catchment area)...")
    wbe.d8_flow_accumulation(f"{output_dir}/dem_breached.tif", f"{output_dir}/d8_flow_accum_sca.tif", out_type="sca")

    # D-infinity flow accumulation
    print("  - D-infinity flow accumulation...")
    wbe.d_inf_flow_accumulation(f"{output_dir}/dem_breached.tif", f"{output_dir}/dinf_flow_accum.tif", out_type="cells")

    # D-infinity flow accumulation (specific catchment area)
    print("  - D-infinity flow accumulation (specific catchment area)...")
    wbe.d_inf_flow_accumulation(f"{output_dir}/dem_breached.tif", f"{output_dir}/dinf_flow_accum_sca.tif", out_type="sca")

    # FD8 flow accumulation
    print("  - FD8 flow accumulation...")
    wbe.fd8_flow_accumulation(f"{output_dir}/dem_breached.tif", f"{output_dir}/fd8_flow_accum.tif", out_type="cells")

    # ========================================================================
    # 4. WATERSHED DELINEATION
    # ========================================================================
    print_step(4, 9, "Watershed Delineation")

    # First extract streams (needed for hillslopes and subbasins)
    print("  - Extracting streams for watershed analysis...")
    wbe.extract_streams(f"{output_dir}/d8_flow_accum.tif", f"{output_dir}/streams_temp.tif", threshold=1000)

    # Drainage basins
    print("  - Extracting drainage basins...")
    wbe.basins(f"{output_dir}/d8_pointer.tif", f"{output_dir}/basins.tif")

    # Hillslopes (requires streams raster)
    print("  - Extracting hillslopes...")
    wbe.hillslopes(f"{output_dir}/d8_pointer.tif", f"{output_dir}/streams_temp.tif", f"{output_dir}/hillslopes.tif")

    # Subbasins (requires streams raster)
    print("  - Extracting subbasins...")
    wbe.subbasins(f"{output_dir}/d8_pointer.tif", f"{output_dir}/streams_temp.tif", f"{output_dir}/subbasins.tif")

    # ========================================================================
    # 5. STREAM-RELATED METRICS
    # ========================================================================
    print_step(5, 9, "Stream-Related Metrics")

    # Elevation above stream
    print("  - Calculating elevation above stream...")
    wbe.elevation_above_stream(f"{output_dir}/dem_breached.tif", f"{output_dir}/streams_temp.tif", f"{output_dir}/elevation_above_stream.tif")

    # Downslope distance to stream
    print("  - Calculating downslope distance to stream...")
    wbe.downslope_distance_to_stream(f"{output_dir}/dem_breached.tif", f"{output_dir}/streams_temp.tif", f"{output_dir}/distance_to_stream.tif")

    # ========================================================================
    # 6. FLOWPATH ANALYSIS
    # ========================================================================
    print_step(6, 9, "Flowpath Analysis")

    # Average upslope flowpath length
    print("  - Calculating average upslope flowpath length...")
    wbe.average_upslope_flowpath_length(f"{output_dir}/d8_pointer.tif", f"{output_dir}/avg_upslope_flowpath_length.tif")

    # Average flowpath slope
    print("  - Calculating average flowpath slope...")
    wbe.average_flowpath_slope(f"{output_dir}/dem_breached.tif", f"{output_dir}/avg_flowpath_slope.tif")

    # Downslope flowpath length
    print("  - Calculating downslope flowpath length...")
    wbe.downslope_flowpath_length(f"{output_dir}/d8_pointer.tif", f"{output_dir}/downslope_flowpath_length.tif")

    # Maximum upslope flowpath length
    print("  - Calculating maximum upslope flowpath length...")
    wbe.max_upslope_flowpath_length(f"{output_dir}/d8_pointer.tif", f"{output_dir}/max_upslope_flowpath_length.tif")

    # ========================================================================
    # 7. TOPOGRAPHIC WETNESS
    # ========================================================================
    print_step(7, 9, "Topographic Wetness Indices")

    # Topographic wetness index (TWI)
    print("  - Calculating topographic wetness index (TWI)...")
    slope_file = Path("outputs/02_geomorphometry/slope_degrees.tif")
    if slope_file.exists():
        wbe.wetness_index(f"{output_dir}/d8_flow_accum_sca.tif", "outputs/02_geomorphometry/slope_degrees.tif", f"{output_dir}/wetness_index.tif")
    else:
        print("    (Skipped - requires slope from geomorphometry)")

    # ========================================================================
    # 8. STREAM POWER AND EROSION INDICES
    # ========================================================================
    print_step(8, 9, "Stream Power and Erosion Indices")

    # Stream power index
    print("  - Calculating stream power index...")
    if slope_file.exists():
        wbe.stream_power_index(f"{output_dir}/d8_flow_accum_sca.tif", "outputs/02_geomorphometry/slope_degrees.tif", f"{output_dir}/stream_power_index.tif", exponent=1.0)
    else:
        print("    (Skipped - requires slope from geomorphometry)")

    # Sediment transport index
    print("  - Calculating sediment transport index...")
    if slope_file.exists():
        wbe.sediment_transport_index(f"{output_dir}/d8_flow_accum_sca.tif", "outputs/02_geomorphometry/slope_degrees.tif", f"{output_dir}/sediment_transport_index.tif", exponent=1.0)
    else:
        print("    (Skipped - requires slope from geomorphometry)")

    # ========================================================================
    # 9. UTILITY ANALYSES
    # ========================================================================
    print_step(9, 9, "Utility Analyses")

    # Find no-flow cells
    print("  - Finding no-flow cells...")
    wbe.find_no_flow_cells(f"{output_dir}/dem_breached.tif", f"{output_dir}/no_flow_cells.tif")

    # Edge contamination
    print("  - Detecting edge contamination...")
    wbe.edge_contamination(f"{output_dir}/dem_breached.tif", f"{output_dir}/d8_flow_accum.tif", f"{output_dir}/edge_contamination.tif")

    # Elevation above pit
    print("  - Calculating elevation above pit...")
    wbe.elev_above_pit(f"{output_dir}/dem_breached.tif", f"{output_dir}/elev_above_pit.tif")

    print("\n" + "=" * 40)
    print("HYDROLOGY WORKFLOW COMPLETED")
    print(f"Outputs saved to: {output_dir}")
    print("=" * 40)


def main():
    """Main entry point"""
    # Configuration - use command-line args or defaults
    dem_file = sys.argv[1] if len(sys.argv) > 1 else "dem.tif"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/01_hydrology"

    hydrology_workflow(dem_file, output_dir)


if __name__ == "__main__":
    main()
