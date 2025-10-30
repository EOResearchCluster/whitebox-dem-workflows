"""
Fast Raster Visualization Tool

A lightweight TIFF/raster visualization utility without GDAL/rasterio bindings.
Automatically finds raster files by pattern and generates PNG plots with customizable DPI.

Features:
- No GDAL/rasterio dependencies
- Pattern-based file matching (e.g., "slope" finds first matching slope file)
- Auto-generates output filename from input basename
- Customizable DPI for output quality
- Customizable colorbar label
- 300 DPI default for publication quality

Usage:
    python tiffplot.py <raster_file> [--label TEXT] [--dpi DPI]
    python tiffplot.py <pattern> [--label TEXT] [--dpi DPI]

Examples:
    python tiffplot.py slope_degrees.tif                  # Plot specific file
    python tiffplot.py slope                              # Find first file matching "slope"
    python tiffplot.py outputs/01_hydrology/dem_breached.tif
    python tiffplot.py elevation --label "Elevation (m)"
    python tiffplot.py twi --label "TWI" --dpi 150
    pixi run tiffplot slope
    pixi run tiffplot elevation --dpi 200
"""
import sys
import argparse
from pathlib import Path


def find_raster(pattern, search_dir="."):
    """Find first raster file matching pattern"""
    search_path = Path(search_dir)

    # Excluded extensions
    excluded_exts = {'.png', '.svg', '.html', '.ftz', '.ftz_0', '.list', '.xml', '.yrly'}

    # Try exact match first
    if Path(pattern).exists():
        return Path(pattern)

    # Search for pattern match
    for path in search_path.rglob(f"*{pattern}*"):
        if path.is_file() and path.suffix.lower() not in excluded_exts:
            # Prioritize common raster formats
            if path.suffix.lower() in {'.tif', '.tiff', '.img', '.bil', '.asc', '.flt'}:
                return path

    return None


def tiffplot(input_file, output_file=None, label=None, dpi=300):
    """
    Create a high-quality plot of a raster file.

    Args:
        input_file (str): Path to input TIFF/raster file
        output_file (str): Path for output PNG file (auto-generated if None)
        label (str): Label for colorbar (auto-derived from filename if None)
        dpi (int): DPI for output image (default: 300)
    """
    import tifffile
    import numpy as np
    import matplotlib.pyplot as plt

    # Auto-generate output filename and label if not provided
    input_path = Path(input_file)

    if output_file is None:
        output_file = input_path.with_suffix('.png').name
        output_file = Path("outputs") / output_file
        output_file.parent.mkdir(parents=True, exist_ok=True)

    if label is None:
        # Derive label from input filename (without extension)
        label = input_path.stem.replace('_', ' ').title()

    print(f"Reading raster file: {input_file}")
    with tifffile.TiffFile(input_file) as tif:
        dem = tif.asarray()

    print("Creating plot...")
    plt.style.use("seaborn-v0_8-whitegrid")

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot with terrain colormap
    im = ax.imshow(dem, cmap="terrain", interpolation="bilinear")

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, label=label, location="right", shrink=0.5)

    ax.set_xlabel("Easting")
    ax.set_ylabel("Northing")

    print(f"Saving plot as {output_file}")
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.close()


def main():
    """Command-line interface for tiffplot."""
    parser = argparse.ArgumentParser(
        description="Fast TIFF visualization without GDAL/rasterio bindings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s slope_degrees.tif                  # Plot specific file
  %(prog)s slope                              # Find first file matching "slope"
  %(prog)s outputs/01_hydrology/dem_breached.tif
  %(prog)s elevation --label "Elevation (m)"
  %(prog)s twi --label "TWI" --dpi 150
        """
    )

    parser.add_argument(
        'raster',
        help='Raster file path or search pattern'
    )
    parser.add_argument(
        '--label', '-l',
        type=str,
        default=None,
        help='Colorbar label (auto-derived from filename if not specified)'
    )
    parser.add_argument(
        '--dpi', '-d',
        type=int,
        default=300,
        help='DPI for output image (default: 300)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output PNG file path (auto-generated if not specified)'
    )
    parser.add_argument(
        '--search-dir', '-s',
        default='.',
        help='Directory to search for raster files (default: current directory)'
    )

    args = parser.parse_args()

    # Find raster file
    raster_path = find_raster(args.raster, args.search_dir)

    if raster_path is None:
        print(f"❌ Error: No raster file found matching '{args.raster}'", file=sys.stderr)
        print(f"\nSearched in: {Path(args.search_dir).resolve()}", file=sys.stderr)
        print("Tip: Try a different pattern or check the file exists", file=sys.stderr)
        sys.exit(1)

    print(f"📂 Found: {raster_path}")

    # Create plot
    try:
        tiffplot(str(raster_path), output_file=args.output, label=args.label, dpi=args.dpi)
        print("✅ Plot created successfully!")
    except Exception as e:
        print(f"❌ Error creating plot: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
