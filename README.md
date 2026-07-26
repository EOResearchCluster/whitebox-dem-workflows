# WhiteboxTools DEM Analysis Workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WhiteboxTools](https://img.shields.io/badge/WhiteboxTools-Free%20Tools-green.svg)](https://www.whiteboxgeo.com/)

This repository contains four WhiteboxTools-based Digital Elevation Model
(DEM) workflows covering hydrology, geomorphometry, stream networks, and
morphometry, with Bash entry points and Python utilities.

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

## Scope

This repository provides:

- four numbered workflows: `01_hydrology.sh`, `02_geomorphometry.sh`,
  `03_stream_network.sh`, and `04_morphometry.sh`;
- Bash and Python entry points for sequential execution;
- more than 100 requested primary outputs, depending on conditional steps and
  the installed WhiteboxTools build;
- lightweight raster inspection and plotting helpers.

This is a research workflow collection, not a fully verified production
pipeline. Review the limitations below before starting a long run.

## Documentation

- **[INSTALL.md](INSTALL.md)** - Complete installation guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide
- **[FIXES.md](FIXES.md)** - Changelog and fixes documentation
- **[GITHUB_PUSH_INSTRUCTIONS.md](GITHUB_PUSH_INSTRUCTIONS.md)** - Instructions for GitHub setup

## Workflows

### 1. Hydrology (`01_hydrology.sh`)
Requests flow-routing, watershed, and topographic-index outputs.

**Key outputs**: Depression-breached DEMs, flow direction/accumulation, basins, wetness index, stream power

### 2. Geomorphometry (`02_geomorphometry.sh`)
Requests slope, curvature, roughness, landform, and contour outputs.

**Key outputs**: Slope, aspect, hillshades, 10+ curvature types, roughness, geomorphons, contours

### 3. Stream Network Analysis (`03_stream_network.sh`)
Uses hydrology outputs to extract, order, and describe stream networks.

**Key outputs**: Extracted streams, stream ordering (Strahler, Horton, etc.), profiles, distance metrics

### 4. Morphometry (`04_morphometry.sh`)
Requests terrain-texture and multi-scale morphometric outputs.

**Key outputs**: Terrain texture, topographic position (multi-scale), downslope index, upslope metrics

## Requirements

- **Pixi** (package manager): See [INSTALL.md](INSTALL.md)
- **WhiteboxTools**: Auto-installed via pixi
- **Bash**: Standard on macOS/Linux
- **Python 3.11 or 3.12**: Auto-installed with pixi project (for utilities)

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

Pixi workflow tasks use `dem.tif` in the repository root. To select another
input path, call the Bash or Python entry points below.

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

### Python Wrapper
```bash
# Run all workflows
./run_workflows.py --all --dem your_dem.tif

# List available workflows
./run_workflows.py --list

# Run specific workflow
./run_workflows.py --workflow hydrology --dem your_dem.tif
```

## Current Limitations

- No automated tests or CI are configured.
- Current runners may mask an inner WhiteboxTools failure; verify logs
  and expected output files instead of trusting the completion banner.
- The Python wrapper currently passes incorrect positional arguments to the
  stream-network workflow. Run `03_stream_network.sh` directly after hydrology.
- `compare_rasters` in `utils.sh` currently fails to forward its arguments.
- Tool availability depends on the WhiteboxTools build. Version 2.4.0 does not
  provide every command referenced by these scripts, so check long workflows
  with `whitebox_tools --toolhelp=ToolName`.

## Utility Functions
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
```

## Output Structure

| Directory | Contents |
|---|---|
| `outputs/01_hydrology/` | Flow routing, accumulation, basins, and indices |
| `outputs/02_geomorphometry/` | Terrain attributes, curvature, and landforms |
| `outputs/03_stream_network/` | Extracted streams, ordering, and profiles |
| `outputs/04_morphometry/` | Multi-scale terrain and topographic metrics |

Output totals vary with conditional steps, the installed WhiteboxTools build,
and failed tools. Treat expected files—not directory counts—as completion
criteria.

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
