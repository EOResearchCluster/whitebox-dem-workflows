# WhiteboxTools DEM Analysis Workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WhiteboxTools](https://img.shields.io/badge/WhiteboxTools-Free%20Tools-green.svg)](https://www.whiteboxgeo.com/)

Comprehensive geoprocessing workflows for Digital Elevation Model (DEM) analysis using WhiteboxTools. Includes automated workflows for **hydrology**, **geomorphometry**, **stream network analysis**, and **morphometry** using only free/open-source tools.

## Quick Start

```bash
# 1. Install pixi (package manager)
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Clone repository
git clone https://github.com/EOResearchCluster/whitebox-dem-workflows.git
cd whitebox-dem-workflows

# 3. Choose installation method:

# Option A: Global install (simplest)
pixi global install whitebox_tools
./run_all_workflows.sh your_dem.tif

# Option B: Project install (recommended, includes utilities)
pixi install
pixi shell
./run_all_workflows.sh your_dem.tif
```

**📖 See [INSTALL.md](INSTALL.md) for detailed installation instructions**

### Installation Options

| Method | Setup | Utilities (`rp`, etc.) | When to Use |
|--------|-------|------------------------|-------------|
| **Global** | `pixi global install whitebox_tools` | ❌ No | Quick tests |
| **Project** | `pixi install && pixi shell` | ✅ Yes | Daily use (recommended) |

See [SETUP_GUIDE.md](SETUP_GUIDE.md) to choose the right option for you!

## Features

- **100% Free Tools**: Uses only WhiteboxTools open-source functions (no license required)
- **Comprehensive Coverage**: 150+ derived products from a single DEM
- **Production Ready**: Shell scripts with CLI arguments + Python wrapper + Native Python workflows
- **High Performance**: WhiteboxTools automatically uses all CPU cores for optimal speed
- **Native Python Support**: Uses whitebox Python package (open-source WhiteboxTools frontend)
- **Well Documented**: Complete usage examples and tool descriptions

## Documentation

- **[INSTALL.md](INSTALL.md)** - Complete installation guide
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

- **Pixi** (package manager): See [INSTALL.md](INSTALL.md)
- **WhiteboxTools**: Auto-installed via pixi
- **whitebox**: Auto-installed via pixi (for native Python workflows)
- **Bash**: Standard on macOS/Linux (for shell scripts)
- **Python 3.11+**: Auto-installed with pixi project

## Implementation Options

This repository provides **three** ways to run the workflows:

| Method | Technology | Performance | Use Case |
|--------|-----------|-------------|----------|
| **Shell Scripts** | Bash + WhiteboxTools CLI | Good | Cross-platform, simple, proven |
| **Python Wrapper** | Python + subprocess | Good | Orchestration, logging, monitoring |
| **Native Python** | Python + whitebox | Best | Object-oriented API, cleaner code |

### Shell Scripts (`.sh` files)
- Direct calls to WhiteboxTools CLI
- Simplest approach
- Best for quick runs and testing

### Python Wrapper (`run_workflows.py`)
- Wraps shell scripts
- Adds progress monitoring and logging
- Good for automated runs

### Native Python Workflows (`.py` files)
- Uses `whitebox` Python package (open-source)
- Clean object-oriented API
- Better error handling and logging
- **Recommended for Python developers**

## Usage

### Using Pixi Tasks (Recommended)
```bash
# Install dependencies first
pixi install

# Run all workflows
pixi run run-all

# Run individual workflows
pixi run hydrology
pixi run geomorphometry
pixi run stream-network
pixi run morphometry
```

### Direct Script Execution
```bash
# Run all workflows
./run_all_workflows.sh your_dem.tif

# Run individual workflows
./01_hydrology.sh your_dem.tif
./02_geomorphometry.sh your_dem.tif
./03_stream_network.sh your_dem.tif
./04_morphometry.sh your_dem.tif
```

> **Note for WSL users**: Use `pixi run` commands instead of direct script execution to ensure WhiteboxTools is in your PATH.

### Python Wrapper (calls shell scripts)
```bash
# Run all workflows
./run_workflows.py --all --dem your_dem.tif

# List available workflows
./run_workflows.py --list

# Run specific workflow
./run_workflows.py --workflow hydrology --dem your_dem.tif
```

### Native Python Workflows (using whitebox package)
```bash
# Run individual workflows using native Python API
pixi run hydrology-py
pixi run geomorphometry-py
pixi run stream-network-py
pixi run morphometry-py

# Or directly
python 01_hydrology.py dem.tif outputs/01_hydrology
python 02_geomorphometry.py dem.tif outputs/02_geomorphometry
python 03_stream_network.py dem.tif outputs/01_hydrology outputs/03_stream_network
python 04_morphometry.py dem.tif outputs/04_morphometry outputs/02_geomorphometry

# Show help for any workflow
python 01_hydrology.py --help
```

> **Note**: The native Python workflows use the `whitebox` package (open-source frontend)
> which provides a clean Pythonic API for WhiteboxTools with better error handling and
> progress monitoring compared to calling shell scripts directly.

> **Note**: WhiteboxTools automatically uses all available CPU cores for each tool,
> so workflows run sequentially for optimal performance. Running multiple workflows
> simultaneously would cause CPU contention and slow things down.

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
