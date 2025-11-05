#!/usr/bin/env python3
"""
MORPHOMETRY AND TERRAIN ANALYSIS WORKFLOW
Advanced morphometric and terrain analysis using WhiteboxTools
Usage: python 04_morphometry.py [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]
"""

import sys
from pathlib import Path
from whitebox_workflows import WbEnvironment


def print_step(step, total, message):
    """Print step progress"""
    print(f"\n[{step}/{total}] {message}...")


def morphometry_workflow(dem_file, output_dir, geomorph_dir):
    """Run complete morphometry workflow"""

    # Check if DEM exists
    dem_path = Path(dem_file)
    if not dem_path.exists():
        print(f"ERROR: DEM file not found: {dem_file}")
        print(f"Usage: {sys.argv[0]} [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]")
        print(f"Example: {sys.argv[0]} mydem.tif outputs/04_morphometry outputs/02_geomorphometry")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 40)
    print("MORPHOMETRY WORKFLOW STARTED")
    print(f"Input DEM: {dem_file}")
    print(f"Output Directory: {output_dir}")
    print("=" * 40)

    # Initialize WhiteboxTools environment
    wbe = WbEnvironment()

    # 1. ELEVATION DERIVATIVES
    print_step(1, 10, "Elevation Derivatives")

    print("  - Calculating elevation statistics...")
    wbe.raster_histogram(dem_file, f"{output_dir}/elevation_histogram.html")

    print("  - Calculating standard deviation of elevation...")
    wbe.std_dev_filter(dem_file, f"{output_dir}/elevation_stddev.tif", filterx=11, filtery=11)

    print("  - Calculating elevation range...")
    wbe.range_filter(dem_file, f"{output_dir}/elevation_range.tif", filterx=11, filtery=11)

    # 2. SLOPE DERIVATIVES
    print_step(2, 10, "Slope Derivatives")

    # Check if geomorphometry outputs exist, otherwise create slope
    slope_file = Path(f"{geomorph_dir}/slope_degrees.tif")
    if not slope_file.exists():
        print("  - Creating slope (degrees)...")
        wbe.slope(dem_file, f"{output_dir}/slope_degrees.tif", units="degrees")
        slope_file_path = f"{output_dir}/slope_degrees.tif"
    else:
        slope_file_path = f"{geomorph_dir}/slope_degrees.tif"

    print("  - Calculating slope standard deviation...")
    wbe.std_dev_filter(slope_file_path, f"{output_dir}/slope_stddev.tif", filterx=11, filtery=11)

    print("  - Calculating slope range...")
    wbe.range_filter(slope_file_path, f"{output_dir}/slope_range.tif", filterx=11, filtery=11)

    # 3. TERRAIN TEXTURE AND PATTERN
    print_step(3, 10, "Terrain Texture and Pattern")

    print("  - Calculating edge density...")
    wbe.edge_density(dem_file, f"{output_dir}/edge_density.tif")

    # 4. FEATURE PRESERVATION SMOOTHING
    print_step(4, 10, "Feature Preservation Smoothing")

    print("  - Applying feature preserving smoothing...")
    wbe.feature_preserving_smoothing(dem_file, f"{output_dir}/dem_smoothed.tif", filter=11)

    print("  - Applying Gaussian filter...")
    wbe.gaussian_filter(dem_file, f"{output_dir}/dem_gaussian.tif", sigma=1.5)

    print("  - Applying mean filter...")
    wbe.mean_filter(dem_file, f"{output_dir}/dem_mean_filtered.tif", filterx=5, filtery=5)

    print("  - Applying median filter...")
    wbe.median_filter(dem_file, f"{output_dir}/dem_median_filtered.tif", filterx=5, filtery=5)

    # 5. RELATIVE TOPOGRAPHIC POSITION
    print_step(5, 10, "Relative Topographic Position")

    print("  - Calculating relative topographic position (multiple scales)...")
    for scale in [3, 5, 11, 21, 51]:
        print(f"    Scale: {scale}x{scale} cells")
        wbe.dev_from_mean_elev(dem_file, f"{output_dir}/rel_topo_pos_{scale}x{scale}.tif",
                              filterx=scale, filtery=scale)

    # 6. DOWNSLOPE INDEX
    print_step(6, 10, "Downslope Index")

    print("  - Calculating downslope index...")
    wbe.downslope_index(dem_file, f"{output_dir}/downslope_index.tif")

    # 7. MULTISCALE TOPOGRAPHIC METRICS
    print_step(7, 10, "Multiscale Topographic Metrics")

    print("  - Calculating multiscale elevation percentile...")
    for scale in [5, 10, 20]:
        print(f"    Scale: {scale} cells radius")
        filter_size = scale * 2 + 1
        wbe.elev_percentile(dem_file, f"{output_dir}/elev_percentile_scale{scale}.tif",
                           filterx=filter_size, filtery=filter_size)

    # 8. ASPECT-BASED MORPHOMETRY
    print_step(8, 10, "Aspect-Based Morphometry")

    # Aspect if not exists
    aspect_file = Path(f"{geomorph_dir}/aspect.tif")
    if not aspect_file.exists():
        print("  - Creating aspect...")
        wbe.aspect(dem_file, f"{output_dir}/aspect.tif")

    print("  - Calculating linear aspect...")
    wbe.aspect(dem_file, f"{output_dir}/aspect_linear.tif")

    # 9. PROFILE AND TANGENTIAL CURVATURE COMBINATIONS
    print_step(9, 10, "Profile and Tangential Curvature Combinations")

    # Profile curvature if not exists
    if not Path(f"{geomorph_dir}/profile_curvature.tif").exists():
        print("  - Creating profile curvature...")
        wbe.profile_curvature(dem_file, f"{output_dir}/profile_curvature.tif")

    # Plan curvature if not exists
    if not Path(f"{geomorph_dir}/plan_curvature.tif").exists():
        print("  - Creating plan curvature...")
        wbe.plan_curvature(dem_file, f"{output_dir}/plan_curvature.tif")

    print("  - Skipping licensed tools (Unsphericity, ShapeIndex)")

    # 10. FLOW TOPOLOGY METRICS
    print_step(10, 10, "Flow Topology Metrics")

    print("  - Calculating max upslope elevation change...")
    wbe.max_upslope_elev_change(dem_file, f"{output_dir}/max_upslope_elev_change.tif")

    print("  - Calculating number of upslope neighbours...")
    wbe.num_upslope_neighbours(dem_file, f"{output_dir}/num_upslope_neighbours.tif")

    print("  - Skipping licensed tool (ImpoundmentSizeIndex)")

    print("\n" + "=" * 40)
    print("MORPHOMETRY WORKFLOW COMPLETED")
    print(f"Outputs saved to: {output_dir}")
    print("=" * 40)


def main():
    """Main entry point"""
    dem_file = sys.argv[1] if len(sys.argv) > 1 else "dem.tif"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/04_morphometry"
    geomorph_dir = sys.argv[3] if len(sys.argv) > 3 else "outputs/02_geomorphometry"

    morphometry_workflow(dem_file, output_dir, geomorph_dir)


if __name__ == "__main__":
    main()
