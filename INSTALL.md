# Installation Guide

Complete installation guide for WhiteboxTools DEM Analysis Workflows.

## Table of Contents
- [Quick Start](#quick-start)
- [Option 1: Global Installation](#option-1-global-installation-simplest)
- [Option 2: Pixi Project (Recommended)](#option-2-pixi-project-recommended)
- [Verify Installation](#verify-installation)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

**TL;DR**: Install pixi, then choose global OR project installation.

```bash
# 1. Install pixi (one-time setup)
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Clone this repository
git clone https://github.com/EOResearchCluster/whitebox-dem-workflows.git
cd whitebox-dem-workflows

# 3. Choose one of the following:

# Option A: Global install (simple, always available)
pixi global install whitebox_tools

# Option B: Project install (recommended, isolated environment)
pixi install
pixi shell  # Activate environment
```

---

## Installing Pixi

Pixi is a modern package manager that makes dependency management easy. Install it once, use it everywhere.

### macOS / Linux

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Windows (PowerShell)

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Verify Pixi Installation

```bash
pixi --version
```

You should see something like: `pixi 0.xx.x`

### Manual Installation

If the automatic installer doesn't work, see: https://pixi.sh/latest/#installation

---

## Option 1: Global Installation (Simplest)

Install WhiteboxTools globally - it will be available system-wide.

### Install

```bash
pixi global install whitebox_tools
```

### Verify

```bash
whitebox_tools --version
```

### Pros & Cons

✅ **Pros:**
- Simple, one command
- Available everywhere
- No need to activate environment

❌ **Cons:**
- Only WhiteboxTools (no Python utilities like `rp`)
- Can't use `utils.sh` functions (need rasterio)
- Version conflicts with other projects possible

### Usage

```bash
# Just run the workflows
./run_all_workflows.sh dem.tif

# Or individual workflows
./01_hydrology.sh dem.tif
```

---

## Option 2: Pixi Project (Recommended)

Create an isolated project environment with all dependencies including Python utilities.

### Install

```bash
# In the project directory
pixi install
```

This will install:
- WhiteboxTools
- Python 3.11+
- rasterio (for viewing rasters)
- matplotlib (for visualization)
- All dependencies from `pixi.toml`

### Activate Environment

Every time you want to use the project, activate the environment:

```bash
pixi shell
```

You'll see your prompt change to indicate you're in the pixi environment:
```
(whitebox-dem-workflows) user@machine:~/whitebox-dem-workflows$
```

### Verify

```bash
# Inside pixi shell
whitebox_tools --version
python --version
python -c "import rasterio; print('rasterio OK')"
```

### Pros & Cons

✅ **Pros:**
- Isolated environment (won't conflict with other projects)
- Includes all Python dependencies for utilities
- Can use `rp` and other visualization tools
- Can use `utils.sh` functions
- Reproducible across machines
- Lock file ensures exact versions

❌ **Cons:**
- Need to activate environment (`pixi shell`) before use
- Slightly larger disk space usage

### Usage

```bash
# Activate environment
pixi shell

# Load utilities (optional but recommended)
source utils.sh

# Run workflows
./run_all_workflows.sh dem.tif

# Use utilities
rp slope
workflow_status
list_outputs
```

### Exit Environment

```bash
exit  # or Ctrl+D
```

### Development Environment (Optional)

For development work (Jupyter notebooks, IPython), use the dev environment:

```bash
# Install with dev dependencies
pixi install --environment dev

# Activate dev environment
pixi shell --environment dev

# Now you have Jupyter and IPython
jupyter notebook
ipython
```

---

## Verify Installation

### Check WhiteboxTools

```bash
whitebox_tools --version
whitebox_tools --listtools | head -20
```

### Check Python Dependencies (Pixi Project Only)

```bash
pixi shell
python -c "import rasterio, matplotlib; print('✅ All dependencies OK')"
```

### Test Workflow

```bash
# Make sure you have a DEM file named dem.tif
# Or use the --dem flag to specify your DEM

./run_workflows.py --list  # Should list all workflows
```

---

## Troubleshooting

### Pixi command not found

**Problem:** After installing pixi, the command isn't recognized.

**Solution:** Restart your terminal or source your shell config:
```bash
source ~/.bashrc  # or ~/.zshrc for zsh
```

### WhiteboxTools not found (Global Install)

**Problem:** `whitebox_tools: command not found`

**Solution:** Make sure pixi's global bin is in your PATH:
```bash
echo 'export PATH="$HOME/.pixi/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Python errors with utils.sh (Global Install)

**Problem:** `ModuleNotFoundError: No module named 'rasterio'`

**Solution:** Use the pixi project option instead:
```bash
pixi install
pixi shell
source utils.sh
```

### "rp" command not working

**Problem:** `rp: command not found` or path errors

**Solution:** Make sure you:
1. Are in the project directory
2. Have sourced utils.sh: `source utils.sh`
3. Are using the pixi project (not global install)

### Pixi shell activation slow

**Problem:** `pixi shell` takes a long time

**Solution:** This is normal the first time as it downloads dependencies. Subsequent activations are instant.

### Can't find view_raster.py

**Problem:** `view_raster.py not found`

**Solution:** Make sure you're in the project directory:
```bash
cd /path/to/whitebox-dem-workflows
source utils.sh
```

---

## Recommended Setup

For the best experience, we recommend:

1. **Install pixi** (one-time)
2. **Use pixi project** for this workflow (includes all utilities)
3. **Add alias to your shell config** for convenience:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias wbt='cd ~/path/to/whitebox-dem-workflows && pixi shell'
```

Then you can just type `wbt` to activate the environment!

---

## What Gets Installed?

### Global Install
- `whitebox_tools` binary only

### Pixi Project Install
- `whitebox_tools` binary
- Python 3.11+
- `rasterio` (geospatial I/O)
- `matplotlib` (visualization)
- `numpy` (numerical computing)
- All transitive dependencies

### Disk Space

- Pixi itself: ~50 MB
- Global install: ~100 MB
- Project install: ~500 MB (includes Python + all libs)

---

## Updating

### Update Pixi

```bash
pixi self-update
```

### Update Global WhiteboxTools

```bash
pixi global install whitebox_tools --force
```

### Update Project Dependencies

```bash
pixi update
```

---

## Uninstalling

### Remove Global WhiteboxTools

```bash
pixi global uninstall whitebox_tools
```

### Remove Project Environment

```bash
pixi clean
rm -rf .pixi
```

### Remove Pixi Completely

```bash
rm -rf ~/.pixi
# Remove from PATH in ~/.bashrc or ~/.zshrc
```

---

## Next Steps

After installation:

1. **Read [QUICKSTART.md](QUICKSTART.md)** for usage examples
2. **Read [README.md](README.md)** for detailed documentation
3. **Run workflows**: `./run_all_workflows.sh your_dem.tif`
4. **Try utilities**: `source utils.sh && rp slope`

---

## Getting Help

- **Installation issues**: See [Troubleshooting](#troubleshooting) above
- **Pixi documentation**: https://pixi.sh/latest/
- **WhiteboxTools**: https://www.whiteboxgeo.com/
- **Project issues**: https://github.com/EOResearchCluster/whitebox-dem-workflows/issues
