# Changelog

All notable changes to the WhiteboxTools DEM Analysis Workflows project.

## [1.0.0] - 2025-10-17

### Major Updates

#### 🎯 DEM Naming Convention
- **Changed default DEM name** from `DEM5_bbox_Dettelbach.tif` to `dem.tif` for simplicity
- Updated all scripts and documentation to use the new naming convention
- Files updated: all workflow scripts (01-04), `run_workflows.py`, `run_all_workflows.sh`, all documentation

#### 🚀 Pixi Integration
- **Added pixi project support** for reproducible, isolated environments
- Created `pixi.toml` with all dependencies (Python, WhiteboxTools, rasterio, matplotlib, numpy)
- Users can now choose between:
  - **Global install**: Simple, quick (`pixi global install whitebox_tools`)
  - **Pixi project**: Full-featured with utilities (`pixi install && pixi shell`)

#### 📚 New Documentation
- **INSTALL.md**: Comprehensive installation guide
  - Step-by-step pixi installation for macOS/Linux/Windows
  - Detailed instructions for both installation methods
  - Troubleshooting section
  - Verification steps

- **SETUP_GUIDE.md**: Decision helper for choosing installation method
  - Clear comparison between Global vs Project install
  - Use cases and recommendations
  - Quick reference commands
  - Learning path for beginners to advanced users

- **CHANGELOG.md**: This file - tracking all changes

#### 🐛 Bug Fixes

##### Fixed `rp` Command Path Resolution
**Problem**: The `rp` utility failed when called from subdirectories (e.g., `outputs/02_geomorphometry/`)

**Solution**: Updated `utils.sh` to search up the directory tree for `view_raster.py`
- Now works from ANY subdirectory within the project
- Automatically finds the project root
- Passes current directory as search base to Python script

**Example that now works**:
```bash
cd outputs/02_geomorphometry/
source ../../utils.sh
rp slope  # ✅ Works!
```

##### Fixed Python Wrapper Argument Passing
**Problem**: Python wrapper wasn't passing DEM file path and output directories to bash scripts

**Solution**: Updated `run_workflows.py` to build command with proper arguments
- Passes DEM file path as first argument
- Passes output directory as second argument
- For morphometry, also passes geomorphometry directory as third argument

#### 🔄 Removed Misleading Parallel Option

**Problem**: `--parallel` option was misleading - WhiteboxTools already uses all CPU cores internally

**Solution**: Removed `--parallel` option entirely
- Removed from `run_workflows.py`
- Removed `run_parallel()` method
- Renamed `run_sequential()` to `run_all()` (more accurate)
- Updated all documentation to clarify WhiteboxTools auto-parallelization
- Added notes explaining why sequential execution is optimal

**Files updated**: `run_workflows.py`, all documentation

#### 📦 Pixi Tasks
Added convenient pixi tasks for common operations:
```bash
pixi run run-all              # Run all workflows
pixi run hydrology            # Just hydrology
pixi run geomorphometry       # Just geomorphometry
pixi run stream-network       # Just stream network
pixi run morphometry          # Just morphometry
pixi run run-py               # Python wrapper
pixi run list-workflows       # List workflows
pixi run clean                # Clean outputs/logs
```

#### 🌍 Pixi Environments
- **Default environment**: Production dependencies (Python, WhiteboxTools, rasterio, matplotlib)
- **Dev environment**: Includes Jupyter and IPython for development work
  ```bash
  pixi shell --environment dev
  jupyter notebook
  ```

#### 📝 Documentation Updates

**README.md**:
- Added installation options comparison table
- Updated Quick Start with both installation methods
- Added links to INSTALL.md and SETUP_GUIDE.md
- Updated requirements section
- Clarified WhiteboxTools auto-parallelization

**QUICKSTART.md**:
- Added "First Time Setup" section at the top
- Clarified which features need pixi project vs global install
- Updated troubleshooting with pixi instructions
- Added notes about utility requirements

**All Documentation**:
- Replaced all references to `--parallel` with explanation of auto-parallelization
- Updated all code examples to use new DEM naming convention
- Added pixi installation instructions where relevant

#### 🔧 Configuration Updates

**.gitignore**:
- Added `.pixi/` directory exclusion
- Added `pixi.lock` exclusion

**pixi.toml**:
- Fixed deprecated `depends_on` → `depends-on`
- Added `[environments]` section to properly define dev environment
- Removed unused `[activation]` section

### Installation Methods

#### Global Install (Simple)
```bash
pixi global install whitebox_tools
./run_all_workflows.sh dem.tif
```

**Pros**: Simple, one command, always available
**Cons**: No utilities (`rp`, etc.), no Python tools

#### Pixi Project (Recommended)
```bash
pixi install
pixi shell
source utils.sh
./run_all_workflows.sh dem.tif
```

**Pros**: All utilities, isolated environment, reproducible, can use `rp` command
**Cons**: Need to activate shell

### Dependencies

**Production (Default Environment)**:
- Python >=3.11,<3.13
- whitebox_tools (latest)
- rasterio >=1.3
- matplotlib >=3.7
- numpy >=1.24

**Development (Dev Environment)**:
- All production dependencies
- ipython
- jupyter

### Platform Support
- Linux (x86_64)
- macOS (Intel and Apple Silicon)
- Windows (x86_64)

### Breaking Changes
None - all changes are backward compatible. Scripts still work with custom DEM names via command-line arguments.

### Migration Guide

#### From Previous Version

If you were using the old setup:

1. **Update your DEM filename** (optional but recommended):
   ```bash
   mv DEM5_bbox_Dettelbach.tif dem.tif
   ```

2. **Choose installation method**:
   ```bash
   # Option A: Keep using global install (works as before)
   pixi global install whitebox_tools
   
   # Option B: Switch to pixi project for utilities
   pixi install
   pixi shell
   ```

3. **Update any scripts** that hardcoded the old DEM name:
   ```bash
   # Old
   ./run_all_workflows.sh DEM5_bbox_Dettelbach.tif
   
   # New (with dem.tif in directory)
   ./run_all_workflows.sh
   
   # Or with any DEM
   ./run_all_workflows.sh your_custom_dem.tif
   ```

4. **Remove old parallel flag** from any automation:
   ```bash
   # Old
   ./run_workflows.py --parallel --dem mydem.tif
   
   # New
   ./run_workflows.py --all --dem mydem.tif
   ```

### Deprecations
- `--parallel` flag in `run_workflows.py` (removed)

### Known Issues
None at this time.

### Contributors
- EOResearchCluster

### References
- [INSTALL.md](INSTALL.md) - Installation guide
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Choosing installation method
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [README.md](README.md) - Main documentation
- [FIXES.md](FIXES.md) - Technical fixes documentation

---

## Future Enhancements

Planned for future versions:
- [ ] Example DEM dataset for testing
- [ ] GitHub Actions CI/CD
- [ ] Additional visualization utilities
- [ ] Integration with QGIS
- [ ] Docker container option
- [ ] Additional workflow templates

---

**Full Changelog**: https://github.com/EOResearchCluster/whitebox-dem-workflows/commits/main
