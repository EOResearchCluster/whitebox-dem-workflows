# Windows Compatibility Refactoring

## Overview

This repository has been completely refactored to be fully Windows-compatible by eliminating all bash and Linux-specific dependencies. All workflows now use **Python only** with the `whitebox_workflows` package.

## What Changed

### ✅ New Python Workflow Scripts

All bash scripts (`.sh`) have been converted to pure Python (`.py`):

- `01_hydrology.py` - Hydrological analysis (replaces `01_hydrology.sh`)
- `02_geomorphometry.py` - Geomorphometric analysis (replaces `02_geomorphometry.sh`)
- `03_stream_network.py` - Stream network analysis (replaces `03_stream_network.sh`)
- `04_morphometry.py` - Morphometric analysis (replaces `04_morphometry.sh`)

### ✅ Updated Configuration

- **pixi.toml**: All tasks now use Python commands instead of bash
  - Replaced `bash` calls with `python` calls
  - Replaced `rm -rf` with Python's `shutil.rmtree()`
  - Replaced `mkdir -p` with Python's `pathlib.mkdir(parents=True, exist_ok=True)`
  - Updated dependency from `whitebox_tools` to `whitebox_workflows`

- **run_workflows.py**: Updated to call Python scripts instead of bash scripts

### ✅ Line Ending Management

- **`.gitattributes`**: Added to ensure consistent line endings across platforms
  - Python files always use LF (Unix-style)
  - Prevents CRLF issues on Windows

### ✅ Old Bash Scripts Archived

All original bash scripts have been moved to `archive_bash_scripts/` for reference:
- `01_hydrology.sh`
- `02_geomorphometry.sh`
- `03_stream_network.sh`
- `04_morphometry.sh`
- `run_all_workflows.sh`
- `utils.sh`
- `PUSH_TO_GITHUB.sh`

## Usage

### Running Workflows

The usage is now simpler and works identically on Windows, macOS, and Linux:

```bash
# Install dependencies
pixi install

# Run all workflows
pixi run run-all

# Run individual workflows
pixi run hydrology
pixi run geomorphometry
pixi run stream-network
pixi run morphometry

# Or run directly with Python
python 01_hydrology.py dem.tif outputs/01_hydrology
python 02_geomorphometry.py dem.tif outputs/02_geomorphometry
python 03_stream_network.py dem.tif outputs/01_hydrology outputs/03_stream_network
python 04_morphometry.py dem.tif outputs/04_morphometry outputs/02_geomorphometry
```

### Using the Workflow Manager

```bash
# List available workflows
pixi run list-workflows

# Run all workflows with progress tracking
python run_workflows.py --all

# Run a specific workflow
python run_workflows.py --workflow hydrology
```

### Utilities

```bash
# View a raster file
python view_raster.py slope_degrees.tif

# Create a plot
python tiffplot.py elevation

# Clean outputs (cross-platform)
pixi run clean
```

## Benefits

1. **Windows Compatible**: No more newline issues or bash dependencies
2. **Cross-Platform**: Works identically on Windows, macOS, and Linux
3. **Simpler**: Pure Python is easier to maintain and debug
4. **Better Error Handling**: Python provides better error messages
5. **Consistent**: No shell-specific quirks or differences

## Technical Details

### Dependencies

The refactored workflows use:

- **whitebox_workflows**: Python API for WhiteboxTools
- **pathlib**: Cross-platform path handling
- **shutil**: Cross-platform file operations

No bash, sh, or any Unix-specific commands are used anywhere in the codebase.

### Python API Usage

Instead of subprocess calls to `whitebox_tools` CLI:

```python
# OLD (bash/subprocess)
subprocess.run(["whitebox_tools", "--wd=.", "-r=Slope", "--dem=dem.tif", "-o=slope.tif"])

# NEW (Python API)
from whitebox_workflows import WbEnvironment
wbe = WbEnvironment()
wbe.slope("dem.tif", "slope.tif", units="degrees")
```

### Error Handling

All Python scripts include proper error handling:

- Check if input files exist before processing
- Provide helpful error messages
- Exit gracefully with informative messages

## Migration Notes

If you have existing scripts that call the bash versions:

1. Replace `bash 01_hydrology.sh` with `python 01_hydrology.py`
2. Replace `bash 02_geomorphometry.sh` with `python 02_geomorphometry.py`
3. And so on for other scripts

The arguments remain the same:

```bash
# Before
bash 01_hydrology.sh my_dem.tif outputs/hydrology

# After
python 01_hydrology.py my_dem.tif outputs/hydrology
```

## Troubleshooting

### "whitebox_workflows not found"

Install dependencies:

```bash
pixi install
```

### Line Ending Issues (CRLF vs LF)

The `.gitattributes` file ensures Python files always use LF. If you encounter issues:

```bash
# Refresh line endings
git rm --cached -r .
git reset --hard
```

### Permission Errors on Windows

Python scripts don't need to be marked as executable on Windows. Just run them with `python script.py`.

## Summary

This refactoring completely eliminates the Windows newline and bash compatibility issues by:

1. Converting all bash scripts to pure Python
2. Using the `whitebox_workflows` Python API
3. Replacing all bash commands with Python equivalents
4. Adding `.gitattributes` for consistent line endings
5. Updating `pixi.toml` to use Python-only commands

The repository is now fully cross-platform and Windows-friendly! 🎉
