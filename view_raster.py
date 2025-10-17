#!/usr/bin/env python3
"""
Quick Raster Preview Tool

Quickly visualize raster files from WhiteboxTools output with metadata display.
Based on the 'rp' bash function, enhanced with more features.

Usage:
    ./view_raster.py <raster_file>
    ./view_raster.py <pattern>              # Finds first matching file
    ./view_raster.py <raster_file> --cmap viridis
    ./view_raster.py <raster_file> --hillshade
"""

import sys
import argparse
from pathlib import Path
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import numpy as np


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


def get_colormap(raster_name):
    """Select appropriate colormap based on raster type"""
    name_lower = raster_name.lower()

    # Categorize by raster type
    if any(x in name_lower for x in ['hillshade', 'shade']):
        return 'gray'
    elif any(x in name_lower for x in ['slope', 'aspect']):
        return 'viridis'
    elif any(x in name_lower for x in ['curvature', 'curv']):
        return 'RdBu_r'
    elif any(x in name_lower for x in ['flow', 'accum']):
        return 'Blues'
    elif any(x in name_lower for x in ['wetness', 'twi']):
        return 'YlGnBu'
    elif any(x in name_lower for x in ['elevation', 'dem', 'elev']):
        return 'terrain'
    elif any(x in name_lower for x in ['stream', 'river']):
        return 'Blues'
    elif any(x in name_lower for x in ['basin', 'watershed']):
        return 'tab20'
    else:
        return 'cividis'  # Default


def apply_hillshade_overlay(data, azimuth=315, altitude=45):
    """Apply hillshade effect to data"""
    # Calculate hillshade
    x, y = np.gradient(data)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)

    azimuthrad = azimuth * np.pi/180.
    altituderad = altitude * np.pi/180.

    shaded = np.sin(altituderad) * np.sin(slope) + \
             np.cos(altituderad) * np.cos(slope) * \
             np.cos((azimuthrad - np.pi/2.) - aspect)

    return shaded


def view_raster(raster_path, cmap=None, hillshade=False, title=None):
    """View raster file with metadata"""

    # Open raster
    with rasterio.open(raster_path) as src:
        # Print metadata
        print("\n" + "="*60)
        print(f"Raster: {raster_path.name}")
        print("="*60)
        print(f"Driver:       {src.driver}")
        print(f"Size:         {src.width} x {src.height} pixels")
        print(f"Bands:        {src.count}")
        print(f"Data type:    {src.dtypes[0]}")
        print(f"CRS:          {src.crs}")
        print(f"Bounds:       {src.bounds}")
        print(f"Resolution:   {src.res}")
        print(f"NoData:       {src.nodata}")

        # Read data
        data = src.read(1, masked=True)

        # Calculate statistics
        print(f"\nStatistics:")
        print(f"  Min:        {np.nanmin(data):.4f}")
        print(f"  Max:        {np.nanmax(data):.4f}")
        print(f"  Mean:       {np.nanmean(data):.4f}")
        print(f"  Std Dev:    {np.nanstd(data):.4f}")
        print(f"  Valid %:    {(~data.mask).sum() / data.size * 100:.2f}%")
        print("="*60 + "\n")

        # Select colormap
        if cmap is None:
            cmap = get_colormap(raster_path.name)
            print(f"Auto-selected colormap: {cmap}")

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))

        # Apply hillshade if requested
        if hillshade:
            # Show original data
            im = ax.imshow(data, cmap=cmap, alpha=0.7)
            # Overlay hillshade
            shade = apply_hillshade_overlay(data)
            ax.imshow(shade, cmap='gray', alpha=0.3)
        else:
            # Show raster
            show(src, ax=ax, cmap=cmap)
            im = ax.get_images()[0]

        # Add colorbar
        cbar = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.046)
        cbar.set_label(f'Value ({src.dtypes[0]})', rotation=270, labelpad=15)

        # Set title
        if title is None:
            title = f"{raster_path.name}\n{src.width}x{src.height} | {src.crs}"
        ax.set_title(title, fontsize=12, fontweight='bold')

        # Add axis labels
        ax.set_xlabel('Column (pixel)')
        ax.set_ylabel('Row (pixel)')

        # Tight layout
        plt.tight_layout()

        # Show plot
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Quick Raster Preview Tool for WhiteboxTools outputs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s slope_degrees.tif                  # View specific file
  %(prog)s slope                              # Find first file matching "slope"
  %(prog)s outputs/01_hydrology/dem_breached.tif
  %(prog)s hillshade --cmap gray              # Use gray colormap
  %(prog)s elevation --hillshade              # Apply hillshade overlay
  %(prog)s twi --title "Topographic Wetness Index"
        """
    )

    parser.add_argument('raster',
                        help='Raster file path or search pattern')
    parser.add_argument('--cmap', '-c',
                        help='Matplotlib colormap (e.g., viridis, terrain, RdBu_r)')
    parser.add_argument('--hillshade', action='store_true',
                        help='Apply hillshade overlay effect')
    parser.add_argument('--title', '-t',
                        help='Custom plot title')
    parser.add_argument('--search-dir', '-d', default='.',
                        help='Directory to search for raster (default: current)')

    args = parser.parse_args()

    # Find raster file
    raster_path = find_raster(args.raster, args.search_dir)

    if raster_path is None:
        print(f"❌ Error: No raster file found matching '{args.raster}'", file=sys.stderr)
        print(f"\nSearched in: {Path(args.search_dir).resolve()}", file=sys.stderr)
        print("\nTip: Try a different pattern or check the file exists", file=sys.stderr)
        sys.exit(1)

    print(f"📂 Found: {raster_path}")

    # View raster
    try:
        view_raster(raster_path, cmap=args.cmap, hillshade=args.hillshade, title=args.title)
    except Exception as e:
        print(f"❌ Error viewing raster: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
