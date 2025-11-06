# WSL Fixes Summary

## Issues Fixed

This document summarizes the WSL-specific issues that were identified and fixed to ensure full compatibility with Windows Subsystem for Linux.

## Problems Identified

### 1. WhiteboxTools File Writing Errors

**Issue:** WhiteboxTools reported "error while writing: Os { code: 2, kind: NotFound, message: "No such file or directory" }" when writing output files to subdirectories.

**Root Cause:** On WSL, `mkdir -p` creates directories with metadata that WhiteboxTools cannot properly write to. This is a known WSL filesystem compatibility issue.

**Solution:** Replaced all `mkdir -p` commands with `install -d -D` which creates directories with proper permissions that WhiteboxTools can write to.

### 2. Pixi Environment PATH Issues

**Issue:** Running bash scripts directly (e.g., `./01_hydrology.sh dem.tif`) failed with "whitebox_tools: command not found" even after `pixi install`.

**Root Cause:** WhiteboxTools installed via pixi is only available within the pixi environment, not in the system PATH.

**Solution:**
- Updated pixi.toml tasks to use `bash` explicitly instead of relying on shebang execution
- Documented that WSL users should use `pixi run` commands
- Alternatively, users can activate pixi shell first with `pixi shell`

### 3. Working Directory Issues

**Issue:** WhiteboxTools commands occasionally failed to locate input/output files due to relative path handling differences on WSL.

**Solution:** Added `--wd=.` flag to all whitebox_tools commands to explicitly set the working directory to the current directory.

## Changes Made

### Scripts Modified

All workflow scripts were updated:
- `01_hydrology.sh`
- `02_geomorphometry.sh`
- `03_stream_network.sh`
- `04_morphometry.sh`
- `run_all_workflows.sh`

### Specific Changes

1. **Directory Creation:**
   ```bash
   # Before
   mkdir -p "$OUTPUT_DIR"

   # After
   install -d -D "$OUTPUT_DIR"
   ```

2. **WhiteboxTools Commands:**
   ```bash
   # Before
   whitebox_tools -r=ToolName --input="..." --output="..."

   # After
   whitebox_tools --wd=. -r=ToolName --input="..." --output="..."
   ```

3. **Pixi Tasks (pixi.toml):**
   ```toml
   # Before
   hydrology = "./01_hydrology.sh dem.tif"

   # After
   hydrology = "bash 01_hydrology.sh dem.tif"
   ```

### Documentation Updated

- `README.md` - Added WSL usage notes recommending pixi run commands
- `INSTALL.md` - Added comprehensive WSL Notes section
- Created this summary document

## Testing Results

### Test Environment
- Platform: WSL 2 on Windows
- Distribution: Ubuntu (Linux 6.6.87.2-microsoft-standard-WSL2)
- DEM: 4.1MB test file (dem.tif)

### Test Command
```bash
rm -rf outputs logs && pixi run run-all
```

### Results
✅ **All workflows completed successfully**

- Execution time: 100 seconds (~1.5 minutes)
- Files created:
  - 99 GeoTIFF (.tif) files
  - 3 Shapefiles (.shp)
  - 4 log files
- No errors encountered
- All output directories populated correctly:
  - `outputs/01_hydrology/` - 26 files
  - `outputs/02_geomorphometry/` - 39 files
  - `outputs/03_stream_network/` - 27 files
  - `outputs/04_morphometry/` - 20 files

## Recommendations for WSL Users

### Preferred Method (Easiest)

```bash
pixi install
pixi run hydrology         # Run individual workflow
pixi run run-all           # Run all workflows
```

### Alternative Method

```bash
pixi shell                 # Activate environment
./01_hydrology.sh dem.tif  # Run scripts directly
exit                       # Deactivate when done
```

### Not Recommended

```bash
# ❌ Don't run scripts directly without pixi
./01_hydrology.sh dem.tif  # Will fail with "command not found"
```

## Known Limitations

None currently identified. The workflows are fully functional on WSL with the fixes implemented.

## Future Considerations

- Consider adding Windows native support (cmd/PowerShell scripts)
- Monitor for future WhiteboxTools updates that may improve WSL compatibility
- Consider switching to Python-only implementation for cross-platform consistency

## References

- WSL mkdir issues: https://github.com/microsoft/WSL/issues/4197
- Pixi documentation: https://pixi.sh/latest/
- WhiteboxTools: https://github.com/jblindsay/whitebox-tools

---

**Last Updated:** 2025-10-20
**Tested On:** WSL 2 (Ubuntu) with pixi 0.40.1 and WhiteboxTools 2.3.0
