# Setup Guide

Quick guide to get started with WhiteboxTools DEM Analysis Workflows.

## 🎯 Choose Your Setup

We offer **two installation methods** to fit your workflow:

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Global Install** | Quick testing, simple use | ✅ Simple<br>✅ Always available<br>✅ One command | ❌ No utilities (`rp`, etc.)<br>❌ No Python tools |
| **Pixi Project** | Daily use, full features | ✅ All utilities included<br>✅ Isolated environment<br>✅ Reproducible<br>✅ Can use `rp` command | ❌ Need to activate shell<br>❌ Slightly more setup |

**💡 Recommendation:** Use **Pixi Project** for the best experience!

---

## 🚀 Global Install (Quick & Simple)

Perfect for: Quick tests, one-off analyses, simple workflows

### Installation

```bash
# 1. Install pixi (one-time)
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc  # or restart terminal

# 2. Install WhiteboxTools globally
pixi global install whitebox_tools

# 3. Clone repository
git clone https://github.com/EOResearchCluster/whitebox-dem-workflows.git
cd whitebox-dem-workflows

# 4. Run workflows
./run_all_workflows.sh dem.tif
```

### What You Can Do

✅ Run all workflow scripts (`.sh` files)
✅ Run Python wrapper (`run_workflows.py`)
✅ Basic DEM processing

### What You Can't Do

❌ Use `rp` command (requires rasterio)
❌ Use `utils.sh` functions (requires Python dependencies)
❌ Use `view_raster.py` (requires rasterio)

---

## 🎨 Pixi Project (Recommended)

Perfect for: Daily use, research projects, full feature set

### Installation

```bash
# 1. Install pixi (one-time)
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc  # or restart terminal

# 2. Clone repository
git clone https://github.com/EOResearchCluster/whitebox-dem-workflows.git
cd whitebox-dem-workflows

# 3. Install project dependencies
pixi install

# 4. Activate environment
pixi shell
```

### What You Can Do

✅ Everything from Global Install, PLUS:
✅ Use `rp slope` for quick raster visualization
✅ Use all `utils.sh` functions
✅ Use Python utilities (`view_raster.py`)
✅ Isolated, reproducible environment
✅ Access to pixi tasks

### Daily Workflow

```bash
# Navigate to project
cd ~/whitebox-dem-workflows

# Activate environment (do this each session)
pixi shell

# Load utilities (optional but recommended)
source utils.sh

# Now you can use everything!
rp slope
workflow_status
./run_all_workflows.sh dem.tif
```

### Convenient Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias wbt='cd ~/path/to/whitebox-dem-workflows && pixi shell'
```

Then just type `wbt` to activate!

---

## 📦 Pixi Tasks (Project Only)

When using pixi project, you get convenient tasks:

```bash
# List all tasks
pixi task list

# Run workflows
pixi run run-all              # Run all workflows
pixi run hydrology            # Just hydrology
pixi run geomorphometry       # Just geomorphometry

# Python wrapper
pixi run run-py               # Run with Python
pixi run list-workflows       # List available workflows

# Utilities
pixi run clean                # Clean outputs and logs
```

---

## 🔧 Utilities Comparison

### With Global Install

```bash
# You can only run workflows
./run_all_workflows.sh dem.tif
./01_hydrology.sh dem.tif
python run_workflows.py --all
```

### With Pixi Project

```bash
# Run workflows PLUS utilities
./run_all_workflows.sh dem.tif

# Load utilities
source utils.sh

# Quick raster preview (works from ANY directory!)
cd outputs/02_geomorphometry/
rp slope                      # 🎉 Finds and displays slope raster!
rp hillshade --cmap gray

# Back to project root
cd ../..
rp elevation --hillshade      # Searches all outputs

# Check status
workflow_status

# List outputs
list_outputs
list_outputs hydrology

# Compare rasters
compare_rasters dem.tif outputs/01_hydrology/dem_breached.tif

# Quick workflow
quick_run hydrology dem.tif
```

---

## 🐛 Troubleshooting

### "rp: command not found"

**Cause:** Using global install OR haven't sourced utils.sh

**Fix:**
```bash
# Make sure you're using pixi project
pixi shell
source utils.sh
rp slope
```

### "view_raster.py not found" from subdirectory

**Cause:** Old version of utils.sh

**Fix:** The new `utils.sh` automatically searches up the directory tree! Just make sure you're within the project directory structure.

```bash
cd /Volumes/eorc/GitHub/whitebox-dem-workflows/outputs/02_geomorphometry/
source ../../utils.sh
rp slope  # ✅ Works now!
```

### "ModuleNotFoundError: No module named 'rasterio'"

**Cause:** Using global install

**Fix:** Switch to pixi project:
```bash
pixi install
pixi shell
source utils.sh
```

### "whitebox_tools: command not found"

**Cause:** Pixi not installed or not in PATH

**Fix:**
```bash
# Install pixi
curl -fsSL https://pixi.sh/install.sh | bash

# Restart terminal or:
source ~/.bashrc

# Verify
pixi --version
```

---

## 📚 Documentation Map

- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - This file (choosing installation method)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick commands and examples
- **[README.md](README.md)** - Full project documentation
- **[FIXES.md](FIXES.md)** - Changelog and fixes

---

## 🎓 Learning Path

### Beginner

1. Start with **Global Install**
2. Run `./run_all_workflows.sh dem.tif`
3. Explore outputs in QGIS

### Intermediate

1. Switch to **Pixi Project**
2. Load utilities: `source utils.sh`
3. Use `rp` to preview rasters
4. Use `workflow_status` and `list_outputs`

### Advanced

1. Customize workflows in `.sh` files
2. Use pixi tasks for automation
3. Create custom utilities
4. Integrate with other tools

---

## ✨ Quick Reference

```bash
# === GLOBAL INSTALL ===
pixi global install whitebox_tools
./run_all_workflows.sh dem.tif

# === PIXI PROJECT ===
pixi install && pixi shell
source utils.sh
rp slope
./run_all_workflows.sh dem.tif

# === COMMON TASKS ===
# List workflows
./run_workflows.py --list

# Run specific workflow
./01_hydrology.sh dem.tif

# Check status (project only)
workflow_status

# Quick preview (project only)
rp hillshade
rp elevation --cmap terrain

# Clean outputs
rm -rf outputs/ logs/
# or with pixi: pixi run clean
```

---

## 🆘 Still Need Help?

1. Check [INSTALL.md](INSTALL.md) for detailed installation steps
2. Check [QUICKSTART.md](QUICKSTART.md) for usage examples
3. Check [Troubleshooting](#troubleshooting) section above
4. Open an issue: https://github.com/EOResearchCluster/whitebox-dem-workflows/issues

---

**Happy mapping! 🗺️**
