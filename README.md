# WhiteboxTools DEM Analysis Workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WhiteboxTools](https://img.shields.io/badge/WhiteboxTools-Free%20Tools-green.svg)](https://www.whiteboxgeo.com/)

Comprehensive geoprocessing workflows for Digital Elevation Model (DEM) analysis using WhiteboxTools. Includes automated workflows for **hydrology**, **geomorphometry**, **stream network analysis**, and **morphometry** using only free/open-source tools.

## Quick Start

```bash
# Install WhiteboxTools
pixi global install whitebox_tools

# Run all workflows
./run_all_workflows.sh your_dem.tif

# Or run with Python (parallel processing)
./run_workflows.py --parallel --dem your_dem.tif
```

## Features

- **100% Free Tools**: Uses only WhiteboxTools open-source functions (no license required)
- **Comprehensive Coverage**: 150+ derived products from a single DEM
- **Production Ready**: Shell scripts with CLI arguments + Python wrapper
- **Parallel Execution**: Python wrapper supports parallel processing
- **Well Documented**: Complete usage examples and tool descriptions

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide
- **[FIXES.md](FIXES.md)** - Changelog and fixes documentation
- **[GITHUB_PUSH_INSTRUCTIONS.md](GITHUB_PUSH_INSTRUCTIONS.md)** - Instructions for GitHub setup

## Workflows

### 1. Hydrology (`01_hydrology.sh`)
Complete hydrological analysis including flow routing, watershed delineation, and topographic indices.

**Key outputs**: Depression-breached DEMs, flow direction/accumulation, basins, wetness index, stream power

### 2. Geomorphometry (`02_geomorphometry.sh`)
Comprehensive terrain attribute analysis including slope, curvatures, roughness, and landform classification.

**Key outputs**: Slope, aspect, hillshades, 10+ curvature types, roughness, geomorphons, contours

### 3. Stream Network Analysis (`03_stream_network.sh`)
Detailed stream network extraction, ordering, and analysis.

**Key outputs**: Extracted streams, stream ordering (Strahler, Horton, etc.), profiles, distance metrics

### 4. Morphometry (`04_morphometry.sh`)
Advanced morphometric analysis including terrain texture and multi-scale metrics.

**Key outputs**: Terrain texture, topographic position (multi-scale), downslope index, upslope metrics

## Requirements

- **WhiteboxTools**: `pixi global install whitebox_tools`
- **Bash**: Standard on macOS/Linux
- **Python 3.6+**: Optional (for parallel execution)

## Usage

### Run All Workflows
```bash
./run_all_workflows.sh your_dem.tif
```

### Run Individual Workflows
```bash
./01_hydrology.sh your_dem.tif
./02_geomorphometry.sh your_dem.tif
./03_stream_network.sh your_dem.tif
./04_morphometry.sh your_dem.tif
```

### Python Wrapper
```bash
# Run in parallel (fastest)
./run_workflows.py --parallel --dem your_dem.tif

# List available workflows
./run_workflows.py --list

# Run specific workflow
./run_workflows.py --workflow hydrology --dem your_dem.tif
```

### Utility Functions
```bash
# Load utilities
source utils.sh

# Quick raster preview
rp slope                        # View any raster matching "slope"
rp hillshade --cmap gray        # Custom colormap
rp dem --hillshade              # Apply hillshade overlay

# Check workflow status
workflow_status                 # See what's completed

# List outputs
list_outputs                    # All workflows
list_outputs hydrology          # Specific workflow

# Compare rasters
compare_rasters dem.tif dem_breached.tif
```

## Output Structure

```
outputs/
├── 01_hydrology/          # ~30 files
├── 02_geomorphometry/     # ~50 files
├── 03_stream_network/     # ~25 files
└── 04_morphometry/        # ~30 files
```

## Citation

If you use these workflows in your research, please cite:

**WhiteboxTools:**
```
Lindsay, J. B. (2016). Whitebox GAT: A case study in geomorphometric analysis.
Computers & Geosciences, 95, 75-84.
```

**This Repository:**
```
EOResearchCluster. (2025). WhiteboxTools DEM Analysis Workflows.
GitHub: https://github.com/EOResearchCluster/whitebox-dem-workflows
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Open an issue on GitHub
- **Documentation**: See QUICKSTART.md and FIXES.md
- **WhiteboxTools**: https://github.com/jblindsay/whitebox-tools

---

**Made with ❤️ by EOResearchCluster**
