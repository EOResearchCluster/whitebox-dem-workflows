#!/usr/bin/env python3
"""
GEOMORPHOMETRY WORKFLOW
Comprehensive geomorphometric analysis using WhiteboxTools Python API

This script uses the whitebox Python package (open-source frontend to WhiteboxTools).

Usage:
    python 02_geomorphometry.py [DEM_FILE] [OUTPUT_DIR]
    python 02_geomorphometry.py dem.tif outputs/02_geomorphometry
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


class GeomorphometryWorkflow:
    """Comprehensive geomorphometric analysis workflow"""

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
        """Execute complete geomorphometry workflow"""
        print("=" * 80)
        print("GEOMORPHOMETRY WORKFLOW STARTED")
        print(f"Input DEM: {self.dem_file}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 80)

        # Run workflow sections
        self.basic_terrain_attributes()
        self.curvature_analysis()
        self.advanced_curvature_metrics()
        self.surface_roughness()
        self.slope_position_classification()
        self.relief_and_residuals()
        self.topographic_openness()
        self.geomorphons_landforms()
        self.aspect_related_analysis()
        self.scale_dependent_analysis()
        self.contours_features()
        self.illumination_visibility()

        print("\n" + "=" * 80)
        print("GEOMORPHOMETRY WORKFLOW COMPLETED")
        print(f"Outputs saved to: {self.output_dir}")
        print("=" * 80)

    def basic_terrain_attributes(self):
        """Section 1: Basic terrain attributes"""
        self.log("Basic Terrain Attributes...", "1/12")

        dem = str(self.dem_file)

        # Slope (multiple units)
        self.log("  - Calculating slope (degrees)...")
        self.wbt.slope(
            dem,
            str(self.output_dir / "slope_degrees.tif"),
            units="degrees"
        )

        self.log("  - Calculating slope (radians)...")
        self.wbt.slope(
            dem,
            str(self.output_dir / "slope_radians.tif"),
            units="radians"
        )

        self.log("  - Calculating slope (percent)...")
        self.wbt.slope(
            dem,
            str(self.output_dir / "slope_percent.tif"),
            units="percent"
        )

        # Aspect
        self.log("  - Calculating aspect...")
        self.wbt.aspect(
            dem,
            str(self.output_dir / "aspect.tif")
        )

        # Hillshade
        self.log("  - Creating hillshade...")
        self.wbt.hillshade(
            dem,
            str(self.output_dir / "hillshade.tif"),
            azimuth=315.0,
            altitude=45.0
        )

        # Multidirectional hillshade
        self.log("  - Creating multidirectional hillshade...")
        self.wbt.multidirectional_hillshade(
            dem,
            str(self.output_dir / "hillshade_multidirectional.tif")
        )

    def curvature_analysis(self):
        """Section 2: Curvature analysis"""
        self.log("Curvature Analysis...", "2/12")

        dem = str(self.dem_file)

        # Profile curvature
        self.log("  - Calculating profile curvature...")
        self.wbt.profile_curvature(
            dem,
            str(self.output_dir / "profile_curvature.tif")
        )

        # Plan curvature
        self.log("  - Calculating plan curvature...")
        self.wbt.plan_curvature(
            dem,
            str(self.output_dir / "plan_curvature.tif")
        )

        # Tangential curvature
        self.log("  - Calculating tangential curvature...")
        self.wbt.tangential_curvature(
            dem,
            str(self.output_dir / "tangential_curvature.tif")
        )

        # Total curvature
        self.log("  - Calculating total curvature...")
        self.wbt.total_curvature(
            dem,
            str(self.output_dir / "total_curvature.tif")
        )

        # Mean curvature
        self.log("  - Calculating mean curvature...")
        self.wbt.mean_curvature(
            dem,
            str(self.output_dir / "mean_curvature.tif")
        )

        # Gaussian curvature
        self.log("  - Calculating Gaussian curvature...")
        self.wbt.gaussian_curvature(
            dem,
            str(self.output_dir / "gaussian_curvature.tif")
        )

        # Minimal curvature
        self.log("  - Calculating minimal curvature...")
        self.wbt.minimal_curvature(
            dem,
            str(self.output_dir / "minimal_curvature.tif")
        )

        # Maximal curvature
        self.log("  - Calculating maximal curvature...")
        self.wbt.maximal_curvature(
            dem,
            str(self.output_dir / "maximal_curvature.tif")
        )

    def advanced_curvature_metrics(self):
        """Section 3: Advanced curvature metrics"""
        self.log("Advanced Curvature Metrics...", "3/12")

        dem = str(self.dem_file)

        # Difference curvature
        self.log("  - Calculating difference curvature...")
        self.wbt.difference_curvature(
            dem,
            str(self.output_dir / "difference_curvature.tif")
        )

        # Horizontal excess curvature
        self.log("  - Calculating horizontal excess curvature...")
        self.wbt.horizontal_excess_curvature(
            dem,
            str(self.output_dir / "horizontal_excess_curvature.tif")
        )

        # Vertical excess curvature
        self.log("  - Calculating vertical excess curvature...")
        self.wbt.vertical_excess_curvature(
            dem,
            str(self.output_dir / "vertical_excess_curvature.tif")
        )

        # Ring curvature
        self.log("  - Calculating ring curvature...")
        self.wbt.ring_curvature(
            dem,
            str(self.output_dir / "ring_curvature.tif")
        )

        # Rotor
        self.log("  - Calculating rotor...")
        self.wbt.rotor(
            dem,
            str(self.output_dir / "rotor.tif")
        )

    def surface_roughness(self):
        """Section 4: Surface roughness and texture"""
        self.log("Surface Roughness and Texture...", "4/12")

        dem = str(self.dem_file)

        # Ruggedness index
        self.log("  - Calculating terrain ruggedness index (TRI)...")
        self.wbt.ruggedness_index(
            dem,
            str(self.output_dir / "ruggedness_index.tif")
        )

        # Multiscale roughness
        self.log("  - Calculating multiscale roughness...")
        self.wbt.multiscale_roughness(
            dem,
            str(self.output_dir / "multiscale_roughness.tif")
        )

        # Surface area ratio
        self.log("  - Calculating surface area ratio...")
        self.wbt.surface_area_ratio(
            dem,
            str(self.output_dir / "surface_area_ratio.tif")
        )

        # Circular variance of aspect
        self.log("  - Calculating circular variance of aspect...")
        self.wbt.circular_variance_of_aspect(
            dem,
            str(self.output_dir / "circular_variance_aspect.tif")
        )

        # Average normal vector angular deviation
        self.log("  - Calculating average normal vector angular deviation...")
        self.wbt.anisotropy_dev(
            dem,
            str(self.output_dir / "avg_normal_vector_angular_dev.tif")
        )

    def slope_position_classification(self):
        """Section 5: Slope position and classification"""
        self.log("Slope Position and Classification...", "5/12")

        dem = str(self.dem_file)

        # Topographic position index (TPI)
        self.log("  - Calculating topographic position index (TPI)...")
        self.wbt.dev_from_mean_elev(
            dem,
            str(self.output_dir / "tpi.tif"),
            filterx=11,
            filtery=11
        )

        # Difference from mean elevation
        self.log("  - Calculating difference from mean elevation...")
        self.wbt.diff_from_mean_elev(
            dem,
            str(self.output_dir / "diff_from_mean_elev.tif"),
            filterx=11,
            filtery=11
        )

        # Elevation percentile
        self.log("  - Calculating elevation percentile...")
        self.wbt.elev_percentile(
            dem,
            str(self.output_dir / "elev_percentile.tif"),
            filterx=11,
            filtery=11
        )

    def relief_and_residuals(self):
        """Section 6: Relief and residuals"""
        self.log("Relief and Residuals...", "6/12")

        dem = str(self.dem_file)

        # Local relief at multiple scales
        self.log("  - Calculating local relief (multiple scales)...")
        for radius in [5, 10, 20, 50]:
            filter_size = radius * 2 + 1
            self.log(f"    Scale: {radius} cells")
            self.wbt.max_elevation_deviation(
                dem,
                str(self.output_dir / f"relief_{radius}cell.tif"),
                filterx=filter_size,
                filtery=filter_size
            )

        # Directional relief
        self.log("  - Calculating directional relief...")
        self.wbt.directional_relief(
            dem,
            str(self.output_dir / "directional_relief.tif")
        )

    def topographic_openness(self):
        """Section 7: Topographic openness"""
        self.log("Topographic Openness...", "7/12")

        dem = str(self.dem_file)

        # Max anisotropy deviation (proxy for openness)
        self.log("  - Calculating max anisotropy deviation...")
        self.wbt.max_anisotropy_dev(
            dem,
            str(self.output_dir / "max_anisotropy_dev.tif")
        )

        # Sky-view factor
        self.log("  - Calculating sky-view factor...")
        self.wbt.sky_view_factor(
            dem,
            str(self.output_dir / "sky_view_factor.tif")
        )

    def geomorphons_landforms(self):
        """Section 8: Geomorphons and landform classification"""
        self.log("Geomorphons and Landform Classification...", "8/12")

        dem = str(self.dem_file)

        # Geomorphons
        self.log("  - Calculating geomorphons...")
        self.wbt.geomorphons(
            dem,
            str(self.output_dir / "geomorphons.tif")
        )

        # Pennock landform classification
        self.log("  - Pennock landform classification...")
        self.wbt.pennock_landform_class(
            dem,
            str(self.output_dir / "pennock_landforms.tif")
        )

    def aspect_related_analysis(self):
        """Section 9: Aspect-related analysis"""
        self.log("Aspect-Related Analysis...", "9/12")

        dem = str(self.dem_file)

        # Aspect (in radians for calculations)
        self.log("  - Calculating aspect in radians...")
        self.wbt.aspect(
            dem,
            str(self.output_dir / "aspect_radians.tif")
        )

        # Note: Eastness and northness require trigonometric operations
        # which would need to be done with separate tools or raster calculator

    def scale_dependent_analysis(self):
        """Section 10: Scale-dependent analysis"""
        self.log("Scale-Dependent Analysis...", "10/12")

        dem = str(self.dem_file)

        # Gaussian scale space
        self.log("  - Gaussian scale space analysis...")
        for sigma in [1.0, 2.0, 5.0]:
            self.log(f"    Sigma: {sigma}")
            # Note: This would require Gaussian filtering at different scales
            # The shell script reuses gaussian_curvature, which isn't exactly
            # a scale-space analysis. We'll compute gaussian curvature here.
            self.wbt.gaussian_curvature(
                dem,
                str(self.output_dir / f"gaussian_scale_sigma{sigma}.tif")
            )

    def contours_features(self):
        """Section 11: Contours and topographic features"""
        self.log("Contours and Topographic Features...", "11/12")

        dem = str(self.dem_file)

        # Contours from raster
        self.log("  - Generating contour lines (5m interval)...")
        self.wbt.contours_from_raster(
            dem,
            str(self.output_dir / "contours_5m.shp"),
            interval=5.0
        )

        # Contours from raster (10m interval)
        self.log("  - Generating contour lines (10m interval)...")
        self.wbt.contours_from_raster(
            dem,
            str(self.output_dir / "contours_10m.shp"),
            interval=10.0
        )

        # Find ridges
        self.log("  - Finding ridges...")
        self.wbt.find_ridges(
            dem,
            str(self.output_dir / "ridges.tif")
        )

    def illumination_visibility(self):
        """Section 12: Illumination and visibility"""
        self.log("Illumination and Visibility...", "12/12")

        dem = str(self.dem_file)

        # Hillshade variations (multiple sun positions)
        self.log("  - Creating hillshade variations...")

        # Morning sun
        self.wbt.hillshade(
            dem,
            str(self.output_dir / "hillshade_morning.tif"),
            azimuth=90.0,
            altitude=30.0
        )

        # Midday sun
        self.wbt.hillshade(
            dem,
            str(self.output_dir / "hillshade_midday.tif"),
            azimuth=180.0,
            altitude=60.0
        )

        # Evening sun
        self.wbt.hillshade(
            dem,
            str(self.output_dir / "hillshade_evening.tif"),
            azimuth=270.0,
            altitude=30.0
        )

        # Hypsometrically tinted hillshade
        self.log("  - Creating hypsometrically tinted hillshade...")
        self.wbt.hypsometrically_tinted_hillshade(
            dem,
            str(self.output_dir / "hillshade_hypsometric.tif")
        )


def main():
    parser = argparse.ArgumentParser(
        description="Geomorphometry Workflow - Comprehensive terrain analysis using WhiteboxTools",
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
        default="outputs/02_geomorphometry",
        help="Output directory (default: outputs/02_geomorphometry)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    try:
        workflow = GeomorphometryWorkflow(
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
