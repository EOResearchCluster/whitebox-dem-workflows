#!/usr/bin/env python3
"""
GEOMORPHOMETRY WORKFLOW
Comprehensive geomorphometric analysis using WhiteboxTools
Usage: python 02_geomorphometry.py [DEM_FILE] [OUTPUT_DIR]
"""

import sys
from pathlib import Path
from whitebox_workflows import WbEnvironment


def print_step(step, total, message):
    """Print step progress"""
    print(f"\n[{step}/{total}] {message}...")


def geomorphometry_workflow(dem_file, output_dir):
    """Run complete geomorphometry workflow"""

    # Check if DEM exists
    dem_path = Path(dem_file)
    if not dem_path.exists():
        print(f"ERROR: DEM file not found: {dem_file}")
        print(f"Usage: {sys.argv[0]} [DEM_FILE] [OUTPUT_DIR]")
        print(f"Example: {sys.argv[0]} mydem.tif outputs/02_geomorphometry")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 40)
    print("GEOMORPHOMETRY WORKFLOW STARTED")
    print(f"Input DEM: {dem_file}")
    print(f"Output Directory: {output_dir}")
    print("=" * 40)

    # Initialize WhiteboxTools environment
    wbe = WbEnvironment()

    # 1. BASIC TERRAIN ATTRIBUTES
    print_step(1, 12, "Basic Terrain Attributes")

    print("  - Calculating slope (degrees)...")
    wbe.slope(dem_file, f"{output_dir}/slope_degrees.tif", units="degrees")

    print("  - Calculating slope (radians)...")
    wbe.slope(dem_file, f"{output_dir}/slope_radians.tif", units="radians")

    print("  - Calculating slope (percent)...")
    wbe.slope(dem_file, f"{output_dir}/slope_percent.tif", units="percent")

    print("  - Calculating aspect...")
    wbe.aspect(dem_file, f"{output_dir}/aspect.tif")

    print("  - Creating hillshade...")
    wbe.hillshade(dem_file, f"{output_dir}/hillshade.tif", azimuth=315.0, altitude=45.0)

    print("  - Creating multidirectional hillshade...")
    wbe.multidirectional_hillshade(dem_file, f"{output_dir}/hillshade_multidirectional.tif")

    # 2. CURVATURE ANALYSIS
    print_step(2, 12, "Curvature Analysis")

    print("  - Calculating profile curvature...")
    wbe.profile_curvature(dem_file, f"{output_dir}/profile_curvature.tif")

    print("  - Calculating plan curvature...")
    wbe.plan_curvature(dem_file, f"{output_dir}/plan_curvature.tif")

    print("  - Calculating tangential curvature...")
    wbe.tangential_curvature(dem_file, f"{output_dir}/tangential_curvature.tif")

    print("  - Calculating total curvature...")
    wbe.total_curvature(dem_file, f"{output_dir}/total_curvature.tif")

    print("  - Calculating mean curvature...")
    wbe.mean_curvature(dem_file, f"{output_dir}/mean_curvature.tif")

    print("  - Calculating Gaussian curvature...")
    wbe.gaussian_curvature(dem_file, f"{output_dir}/gaussian_curvature.tif")

    print("  - Calculating minimal curvature...")
    wbe.minimal_curvature(dem_file, f"{output_dir}/minimal_curvature.tif")

    print("  - Calculating maximal curvature...")
    wbe.maximal_curvature(dem_file, f"{output_dir}/maximal_curvature.tif")

    # 3. ADVANCED CURVATURE METRICS
    print_step(3, 12, "Advanced Curvature Metrics")

    print("  - Calculating difference curvature...")
    wbe.difference_curvature(dem_file, f"{output_dir}/difference_curvature.tif")

    print("  - Calculating horizontal excess curvature...")
    wbe.horizontal_excess_curvature(dem_file, f"{output_dir}/horizontal_excess_curvature.tif")

    print("  - Calculating vertical excess curvature...")
    wbe.vertical_excess_curvature(dem_file, f"{output_dir}/vertical_excess_curvature.tif")

    print("  - Calculating ring curvature...")
    wbe.ring_curvature(dem_file, f"{output_dir}/ring_curvature.tif")

    print("  - Calculating rotor...")
    wbe.rotor(dem_file, f"{output_dir}/rotor.tif")

    # 4. SURFACE ROUGHNESS AND TEXTURE
    print_step(4, 12, "Surface Roughness and Texture")

    print("  - Calculating terrain ruggedness index (TRI)...")
    wbe.ruggedness_index(dem_file, f"{output_dir}/ruggedness_index.tif")

    print("  - Calculating multiscale roughness...")
    wbe.multiscale_roughness(dem_file, f"{output_dir}/multiscale_roughness.tif")

    print("  - Calculating surface area ratio...")
    wbe.surface_area_ratio(dem_file, f"{output_dir}/surface_area_ratio.tif")

    print("  - Calculating circular variance of aspect...")
    wbe.circular_variance_of_aspect(dem_file, f"{output_dir}/circular_variance_aspect.tif")

    print("  - Calculating average normal vector angular deviation...")
    wbe.average_normal_vector_angular_deviation(dem_file, f"{output_dir}/avg_normal_vector_angular_dev.tif")

    # 5. SLOPE POSITION AND CLASSIFICATION
    print_step(5, 12, "Slope Position and Classification")

    print("  - Calculating slope vs elevation percentile...")
    wbe.slope_vs_elevation_plot(dem_file, f"{output_dir}/slope_vs_elevation.html")

    print("  - Calculating topographic position index (TPI)...")
    wbe.dev_from_mean_elev(dem_file, f"{output_dir}/tpi.tif", filterx=11, filtery=11)

    print("  - Calculating difference from mean elevation...")
    wbe.diff_from_mean_elev(dem_file, f"{output_dir}/diff_from_mean_elev.tif", filterx=11, filtery=11)

    print("  - Calculating elevation percentile...")
    wbe.elev_percentile(dem_file, f"{output_dir}/elev_percentile.tif", filterx=11, filtery=11)

    # 6. RELIEF AND RESIDUALS
    print_step(6, 12, "Relief and Residuals")

    print("  - Calculating local relief (multiple scales)...")
    for radius in [5, 10, 20, 50]:
        print(f"    Scale: {radius} cells")
        filter_size = radius * 2 + 1
        wbe.max_elevation_deviation(dem_file, f"{output_dir}/relief_{radius}cell.tif",
                                    filterx=filter_size, filtery=filter_size)

    print("  - Calculating directional relief...")
    wbe.directional_relief(dem_file, f"{output_dir}/directional_relief.tif")

    # 7. TOPOGRAPHIC OPENNESS
    print_step(7, 12, "Topographic Openness")

    print("  - Calculating max anisotropy deviation...")
    wbe.max_anisotropy_dev(dem_file, f"{output_dir}/max_anisotropy_dev.tif")

    print("  - Calculating sky-view factor...")
    wbe.sky_view_factor(dem_file, f"{output_dir}/sky_view_factor.tif")

    # 8. GEOMORPHONS AND LANDFORM CLASSIFICATION
    print_step(8, 12, "Geomorphons and Landform Classification")

    print("  - Calculating geomorphons...")
    wbe.geomorphons(dem_file, f"{output_dir}/geomorphons.tif")

    print("  - Pennock landform classification...")
    wbe.pennock_landform_class(dem_file, f"{output_dir}/pennock_landforms.tif")

    # 9. ASPECT-RELATED ANALYSIS
    print_step(9, 12, "Aspect-Related Analysis")

    print("  - Calculating aspect in radians...")
    wbe.aspect(dem_file, f"{output_dir}/aspect_radians.tif")

    # 10. SCALE-DEPENDENT ANALYSIS
    print_step(10, 12, "Scale-Dependent Analysis")

    print("  - Gaussian scale space analysis...")
    for sigma in [1.0, 2.0, 5.0]:
        print(f"    Sigma: {sigma}")
        wbe.gaussian_curvature(dem_file, f"{output_dir}/gaussian_scale_sigma{sigma}.tif")

    # 11. CONTOURS AND TOPOGRAPHIC FEATURES
    print_step(11, 12, "Contours and Topographic Features")

    print("  - Generating contour lines (5m interval)...")
    wbe.contours_from_raster(dem_file, f"{output_dir}/contours_5m.shp", interval=5.0)

    print("  - Generating contour lines (10m interval)...")
    wbe.contours_from_raster(dem_file, f"{output_dir}/contours_10m.shp", interval=10.0)

    print("  - Finding ridges...")
    wbe.find_ridges(dem_file, f"{output_dir}/ridges.tif")

    # 12. ILLUMINATION AND VISIBILITY
    print_step(12, 12, "Illumination and Visibility")

    print("  - Creating hillshade variations...")

    # Morning sun
    wbe.hillshade(dem_file, f"{output_dir}/hillshade_morning.tif", azimuth=90.0, altitude=30.0)

    # Midday sun
    wbe.hillshade(dem_file, f"{output_dir}/hillshade_midday.tif", azimuth=180.0, altitude=60.0)

    # Evening sun
    wbe.hillshade(dem_file, f"{output_dir}/hillshade_evening.tif", azimuth=270.0, altitude=30.0)

    # Hypsometrically tinted hillshade
    print("  - Creating hypsometrically tinted hillshade...")
    wbe.hypsometrically_tinted_hillshade(dem_file, f"{output_dir}/hillshade_hypsometric.tif")

    print("\n" + "=" * 40)
    print("GEOMORPHOMETRY WORKFLOW COMPLETED")
    print(f"Outputs saved to: {output_dir}")
    print("=" * 40)


def main():
    """Main entry point"""
    dem_file = sys.argv[1] if len(sys.argv) > 1 else "dem.tif"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/02_geomorphometry"

    geomorphometry_workflow(dem_file, output_dir)


if __name__ == "__main__":
    main()
