#!/usr/bin/env python3
"""
MORPHOMETRY AND TERRAIN ANALYSIS WORKFLOW
Advanced morphometric and terrain analysis using WhiteboxTools Python API

This script uses the whitebox Python package (open-source frontend to WhiteboxTools).

Usage:
    python 04_morphometry.py [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]
    python 04_morphometry.py dem.tif outputs/04_morphometry outputs/02_geomorphometry
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


class MorphometryWorkflow:
    """Advanced morphometric and terrain analysis workflow"""

    def __init__(self, dem_file: str, output_dir: str, geomorph_dir: str, verbose: bool = True):
        self.dem_file = Path(dem_file).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.geomorph_dir = Path(geomorph_dir).resolve()
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
        """Execute complete morphometry workflow"""
        print("=" * 80)
        print("MORPHOMETRY WORKFLOW STARTED")
        print(f"Input DEM: {self.dem_file}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 80)

        # Run workflow sections
        self.elevation_derivatives()
        self.slope_derivatives()
        self.terrain_texture()
        self.feature_preservation_smoothing()
        self.relative_topographic_position()
        self.downslope_index()
        self.multiscale_metrics()
        self.aspect_based_morphometry()
        self.curvature_combinations()
        self.flow_topology_metrics()

        print("\n" + "=" * 80)
        print("MORPHOMETRY WORKFLOW COMPLETED")
        print(f"Outputs saved to: {self.output_dir}")
        print("=" * 80)

    def elevation_derivatives(self):
        """Section 1: Elevation derivatives"""
        self.log("Elevation Derivatives...", "1/10")

        dem_str = str(self.dem_file)

        # Elevation histogram
        self.log("  - Calculating elevation statistics...")
        self.wbt.raster_histogram(
            dem_str,
            str(self.output_dir / "elevation_histogram.html")
        )

        # Standard deviation of elevation
        self.log("  - Calculating standard deviation of elevation...")
        self.wbt.std_dev_filter(
            dem_str,
            str(self.output_dir / "elevation_stddev.tif"),
            filterx=11,
            filtery=11
        )

        # Range of elevation
        self.log("  - Calculating elevation range...")
        self.wbt.range_filter(
            dem_str,
            str(self.output_dir / "elevation_range.tif"),
            filterx=11,
            filtery=11
        )

    def slope_derivatives(self):
        """Section 2: Slope derivatives"""
        self.log("Slope Derivatives...", "2/10")

        # Check if geomorphometry outputs exist, otherwise create slope
        slope_path = self.geomorph_dir / "slope_degrees.tif"
        if not slope_path.exists():
            self.log("  - Creating slope (degrees)...")
            self.wbt.slope(
                str(self.dem_file),
                str(self.output_dir / "slope_degrees.tif"),
                units="degrees"
            )
            slope_file = str(self.output_dir / "slope_degrees.tif")
        else:
            slope_file = str(slope_path)

        # Slope standard deviation
        self.log("  - Calculating slope standard deviation...")
        self.wbt.std_dev_filter(
            slope_file,
            str(self.output_dir / "slope_stddev.tif"),
            filterx=11,
            filtery=11
        )

        # Slope range
        self.log("  - Calculating slope range...")
        self.wbt.range_filter(
            slope_file,
            str(self.output_dir / "slope_range.tif"),
            filterx=11,
            filtery=11
        )

    def terrain_texture(self):
        """Section 3: Terrain texture and pattern"""
        self.log("Terrain Texture and Pattern...", "3/10")

        # Edge density
        self.log("  - Calculating edge density...")
        self.wbt.edge_density(
            str(self.dem_file),
            str(self.output_dir / "edge_density.tif")
        )

        # Note: Embankment mapping requires road vector input
        self.log("    (Skipping embankment mapping - requires road vector)")

    def feature_preservation_smoothing(self):
        """Section 4: Feature preservation smoothing"""
        self.log("Feature Preservation Smoothing...", "4/10")

        dem_str = str(self.dem_file)

        # Feature preserving smoothing
        self.log("  - Applying feature preserving smoothing...")
        self.wbt.feature_preserving_smoothing(
            dem_str,
            str(self.output_dir / "dem_smoothed.tif"),
            filter=11
        )

        # Gaussian filter
        self.log("  - Applying Gaussian filter...")
        self.wbt.gaussian_filter(
            dem_str,
            str(self.output_dir / "dem_gaussian.tif"),
            sigma=1.5
        )

        # Mean filter
        self.log("  - Applying mean filter...")
        self.wbt.mean_filter(
            dem_str,
            str(self.output_dir / "dem_mean_filtered.tif"),
            filterx=5,
            filtery=5
        )

        # Median filter
        self.log("  - Applying median filter...")
        self.wbt.median_filter(
            dem_str,
            str(self.output_dir / "dem_median_filtered.tif"),
            filterx=5,
            filtery=5
        )

    def relative_topographic_position(self):
        """Section 5: Relative topographic position"""
        self.log("Relative Topographic Position...", "5/10")

        dem_str = str(self.dem_file)

        # Relative topographic position at multiple scales
        self.log("  - Calculating relative topographic position (multiple scales)...")
        for scale in [3, 5, 11, 21, 51]:
            self.log(f"    Scale: {scale}x{scale} cells")
            self.wbt.dev_from_mean_elev(
                dem_str,
                str(self.output_dir / f"rel_topo_pos_{scale}x{scale}.tif"),
                filterx=scale,
                filtery=scale
            )

    def downslope_index(self):
        """Section 6: Downslope index"""
        self.log("Downslope Index...", "6/10")

        # Downslope index
        self.log("  - Calculating downslope index...")
        self.wbt.downslope_index(
            str(self.dem_file),
            str(self.output_dir / "downslope_index.tif")
        )

    def multiscale_metrics(self):
        """Section 7: Multiscale topographic metrics"""
        self.log("Multiscale Topographic Metrics...", "7/10")

        dem_str = str(self.dem_file)

        # Multiscale elevation percentile
        self.log("  - Calculating multiscale elevation percentile...")
        for scale in [5, 10, 20]:
            self.log(f"    Scale: {scale} cells radius")
            filter_size = scale * 2 + 1
            self.wbt.elev_percentile(
                dem_str,
                str(self.output_dir / f"elev_percentile_scale{scale}.tif"),
                filterx=filter_size,
                filtery=filter_size
            )

    def aspect_based_morphometry(self):
        """Section 8: Aspect-based morphometry"""
        self.log("Aspect-Based Morphometry...", "8/10")

        dem_str = str(self.dem_file)

        # Check if aspect exists in geomorphometry, otherwise create
        aspect_path = self.geomorph_dir / "aspect.tif"
        if not aspect_path.exists():
            self.log("  - Creating aspect...")
            self.wbt.aspect(
                dem_str,
                str(self.output_dir / "aspect.tif")
            )

        # Linear aspect
        self.log("  - Calculating linear aspect...")
        self.wbt.aspect(
            dem_str,
            str(self.output_dir / "aspect_linear.tif")
        )

    def curvature_combinations(self):
        """Section 9: Profile and tangential curvature combinations"""
        self.log("Profile and Tangential Curvature Combinations...", "9/10")

        dem_str = str(self.dem_file)

        # Profile curvature if not exists
        profile_path = self.geomorph_dir / "profile_curvature.tif"
        if not profile_path.exists():
            self.log("  - Creating profile curvature...")
            self.wbt.profile_curvature(
                dem_str,
                str(self.output_dir / "profile_curvature.tif")
            )

        # Plan curvature if not exists
        plan_path = self.geomorph_dir / "plan_curvature.tif"
        if not plan_path.exists():
            self.log("  - Creating plan curvature...")
            self.wbt.plan_curvature(
                dem_str,
                str(self.output_dir / "plan_curvature.tif")
            )

        # Note: Unsphericity and ShapeIndex are licensed tools
        self.log("  - Skipping licensed tools (Unsphericity, ShapeIndex)")

    def flow_topology_metrics(self):
        """Section 10: Flow topology metrics"""
        self.log("Flow Topology Metrics...", "10/10")

        dem_str = str(self.dem_file)

        # Max upslope elevation change
        self.log("  - Calculating max upslope elevation change...")
        self.wbt.max_upslope_elev_change(
            dem_str,
            str(self.output_dir / "max_upslope_elev_change.tif")
        )

        # Number of upslope neighbours
        self.log("  - Calculating number of upslope neighbours...")
        self.wbt.num_upslope_neighbours(
            dem_str,
            str(self.output_dir / "num_upslope_neighbours.tif")
        )

        # Note: ImpoundmentSizeIndex is a licensed tool
        self.log("  - Skipping licensed tool (ImpoundmentSizeIndex)")


def main():
    parser = argparse.ArgumentParser(
        description="Morphometry Workflow - Advanced terrain analysis using WhiteboxTools",
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
        default="outputs/04_morphometry",
        help="Output directory (default: outputs/04_morphometry)",
    )
    parser.add_argument(
        "geomorph_dir",
        nargs="?",
        default="outputs/02_geomorphometry",
        help="Geomorphometry output directory (default: outputs/02_geomorphometry)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    try:
        workflow = MorphometryWorkflow(
            dem_file=args.dem,
            output_dir=args.output_dir,
            geomorph_dir=args.geomorph_dir,
            verbose=not args.quiet,
        )
        workflow.run()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
