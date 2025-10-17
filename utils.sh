#!/bin/bash

# ==============================================================================
# UTILITY FUNCTIONS FOR WHITEBOX DEM WORKFLOWS
# ==============================================================================
#
# Source this file in your shell to get useful functions:
#     source utils.sh
#
# Or add to your ~/.bashrc or ~/.zshrc:
#     source /path/to/whitebox-dem-workflows/utils.sh
# ==============================================================================


# ------------------------------------------------------------------------------
# rp - Raster Preview (Quick visualization)
# ------------------------------------------------------------------------------
# Usage: rp <pattern>
#
# Quickly view a raster file matching the pattern.
# Automatically selects appropriate colormap based on raster type.
#
# Examples:
#   rp slope              # View first file matching "slope"
#   rp hillshade          # View hillshade
#   rp outputs/01_hydrology/dem_breached.tif
# ------------------------------------------------------------------------------
rp() {
    # Check if Python script exists
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local viewer="${script_dir}/view_raster.py"

    if [ ! -f "$viewer" ]; then
        echo "❌ Error: view_raster.py not found at $viewer"
        echo "   Make sure you're in the whitebox-dem-workflows directory"
        return 1
    fi

    # Check for arguments
    if [ $# -eq 0 ]; then
        echo "Usage: rp <pattern> [--cmap COLORMAP] [--hillshade]"
        echo ""
        echo "Examples:"
        echo "  rp slope                   # Find and view first file matching 'slope'"
        echo "  rp hillshade.tif           # View specific file"
        echo "  rp elevation --cmap terrain"
        echo "  rp dem --hillshade"
        return 1
    fi

    # Run viewer
    python3 "$viewer" "$@"
}


# ------------------------------------------------------------------------------
# list_outputs - List all workflow outputs
# ------------------------------------------------------------------------------
# Usage: list_outputs [workflow_name]
#
# List all output files from workflows.
#
# Examples:
#   list_outputs              # List all outputs
#   list_outputs hydrology    # List only hydrology outputs
# ------------------------------------------------------------------------------
list_outputs() {
    local workflow="$1"
    local outputs_dir="outputs"

    if [ ! -d "$outputs_dir" ]; then
        echo "❌ No outputs directory found"
        echo "   Run a workflow first: ./run_all_workflows.sh your_dem.tif"
        return 1
    fi

    if [ -z "$workflow" ]; then
        # List all
        echo "📊 All Workflow Outputs:"
        echo ""
        for dir in "$outputs_dir"/*; do
            if [ -d "$dir" ]; then
                local name=$(basename "$dir")
                local count=$(find "$dir" -type f | wc -l | tr -d ' ')
                local size=$(du -sh "$dir" | cut -f1)
                printf "  %-25s %5s files  %8s\n" "$name" "$count" "$size"
            fi
        done
    else
        # List specific workflow
        local dir="$outputs_dir/*${workflow}*"
        if [ -d "$(echo $dir)" ]; then
            echo "📊 Outputs for: $workflow"
            echo ""
            ls -lh "$dir" | tail -n +2
        else
            echo "❌ No outputs found for: $workflow"
            return 1
        fi
    fi
}


# ------------------------------------------------------------------------------
# compare_rasters - View two rasters side by side
# ------------------------------------------------------------------------------
# Usage: compare_rasters <raster1> <raster2>
#
# Compare two rasters visually.
#
# Examples:
#   compare_rasters dem.tif dem_breached.tif
#   compare_rasters outputs/01_hydrology/dem_filled.tif outputs/01_hydrology/dem_breached.tif
# ------------------------------------------------------------------------------
compare_rasters() {
    if [ $# -ne 2 ]; then
        echo "Usage: compare_rasters <raster1> <raster2>"
        return 1
    fi

    python3 << 'PYTHON_SCRIPT'
import sys
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

r1_path = sys.argv[1]
r2_path = sys.argv[2]

try:
    with rasterio.open(r1_path) as r1, rasterio.open(r2_path) as r2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Plot first raster
        show(r1, ax=ax1, cmap='viridis')
        ax1.set_title(f'{r1_path}\n{r1.width}x{r1.height} | {r1.crs}')

        # Plot second raster
        show(r2, ax=ax2, cmap='viridis')
        ax2.set_title(f'{r2_path}\n{r2.width}x{r2.height} | {r2.crs}')

        plt.tight_layout()
        plt.show()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
python3 -c "$PYTHON_SCRIPT" "$1" "$2"
}


# ------------------------------------------------------------------------------
# workflow_status - Check workflow completion status
# ------------------------------------------------------------------------------
# Usage: workflow_status
#
# Check which workflows have been completed.
# ------------------------------------------------------------------------------
workflow_status() {
    echo "📋 Workflow Status:"
    echo ""

    local workflows=(
        "01_hydrology:outputs/01_hydrology/d8_pointer.tif"
        "02_geomorphometry:outputs/02_geomorphometry/slope_degrees.tif"
        "03_stream_network:outputs/03_stream_network/streams_1000.tif"
        "04_morphometry:outputs/04_morphometry/downslope_index.tif"
    )

    for workflow in "${workflows[@]}"; do
        IFS=':' read -r name check_file <<< "$workflow"
        if [ -f "$check_file" ]; then
            printf "  ✅ %-20s COMPLETED\n" "$name"
        else
            printf "  ❌ %-20s NOT RUN\n" "$name"
        fi
    done

    echo ""
    echo "To run workflows: ./run_all_workflows.sh your_dem.tif"
}


# ------------------------------------------------------------------------------
# clean_outputs - Clean all output directories
# ------------------------------------------------------------------------------
# Usage: clean_outputs
#
# Remove all output files and logs (with confirmation).
# ------------------------------------------------------------------------------
clean_outputs() {
    echo "⚠️  This will delete all outputs and logs!"
    echo ""
    read -p "Are you sure? (y/N): " confirm

    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        rm -rf outputs/
        rm -rf logs/
        echo "✅ Cleaned outputs/ and logs/"
    else
        echo "❌ Cancelled"
    fi
}


# ------------------------------------------------------------------------------
# quick_run - Run specific workflow on specific DEM quickly
# ------------------------------------------------------------------------------
# Usage: quick_run <workflow> <dem>
#
# Quickly run a specific workflow.
#
# Examples:
#   quick_run hydrology mydem.tif
#   quick_run geomorphometry mydem.tif
# ------------------------------------------------------------------------------
quick_run() {
    if [ $# -ne 2 ]; then
        echo "Usage: quick_run <workflow> <dem>"
        echo ""
        echo "Available workflows:"
        echo "  hydrology, geomorphometry, stream_network, morphometry"
        return 1
    fi

    local workflow="$1"
    local dem="$2"

    case "$workflow" in
        hydrology|hydro)
            ./01_hydrology.sh "$dem"
            ;;
        geomorphometry|geomorph)
            ./02_geomorphometry.sh "$dem"
            ;;
        stream_network|stream|streams)
            ./03_stream_network.sh "$dem"
            ;;
        morphometry|morph)
            ./04_morphometry.sh "$dem"
            ;;
        *)
            echo "❌ Unknown workflow: $workflow"
            echo "   Available: hydrology, geomorphometry, stream_network, morphometry"
            return 1
            ;;
    esac
}


# ------------------------------------------------------------------------------
# Show available functions when sourced
# ------------------------------------------------------------------------------
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    echo "✅ WhiteboxTools utility functions loaded!"
    echo ""
    echo "Available commands:"
    echo "  rp <pattern>                      - Quick raster preview"
    echo "  list_outputs [workflow]           - List workflow outputs"
    echo "  compare_rasters <r1> <r2>         - Compare two rasters"
    echo "  workflow_status                   - Check workflow completion"
    echo "  clean_outputs                     - Clean all outputs"
    echo "  quick_run <workflow> <dem>        - Run specific workflow"
    echo ""
    echo "For help: <command> (without arguments)"
fi
