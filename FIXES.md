# Fixes Applied to WhiteboxTools Workflows

## Issues Fixed

### 1. Licensed Tools in 04_morphometry.sh
**Problem**: Several tools require Whitebox extension licenses and were causing errors:
- `Unsphericity` - Licensed (extension)
- `ShapeIndex` - Licensed (extension)
- `MaxUpslopeValue` - Tool doesn't exist (wrong name)
- `ImpoundmentSizeIndex` - Licensed (extension)
- `NumUpslopeCells` - Tool doesn't exist (wrong name)
- `ConvergenceIndex` - Tool doesn't exist

**Solution**:
- Removed all licensed tools
- Replaced `MaxUpslopeValue` with `MaxUpslopeElevChange` (free)
- Replaced `NumUpslopeCells` with `NumUpslopeNeighbours` (free)
- Added clear skip messages for licensed tools

### 2. Hillslopes Tool Panic Error
**Problem**: The Hillslopes tool was crashing with a Rust panic error:
```
thread 'main' panicked at whitebox-raster/src/lib.rs:1361:69:
called `Option::unwrap()` on a `None` value
```

**Root Cause**: The `Hillslopes` tool requires a proper **extracted streams raster file**, not a flow accumulation raster. Same issue with `Subbasins` tool.

**Solution**: Added stream extraction step before watershed delineation:
```bash
# Extract streams first (threshold: 1000 cells)
whitebox_tools -r=ExtractStreams \
  --flow_accum="$OUTPUT_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/streams_temp.tif" \
  --threshold=1000

# Now use extracted streams for Hillslopes
whitebox_tools -r=Hillslopes \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \
  -o="$OUTPUT_DIR/hillslopes.tif"
```

### 2. Stream-Related Metrics Issues
**Problem**: `ElevationAboveStream` and `DownslopeDistanceToStream` were using flow accumulation instead of extracted streams.

**Solution**: Updated both tools to use the extracted streams file:
```bash
whitebox_tools -r=ElevationAboveStream \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \  # <-- Changed
  -o="$OUTPUT_DIR/elevation_above_stream.tif"
```

### 3. No Command-Line Arguments
**Problem**: DEM filename was hardcoded in all scripts.

**Solution**: Added command-line argument support to all workflow scripts:

#### 01_hydrology.sh
```bash
# Usage: ./01_hydrology.sh [DEM_FILE] [OUTPUT_DIR]
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
OUTPUT_DIR="${2:-outputs/01_hydrology}"
```

#### 02_geomorphometry.sh
```bash
# Usage: ./02_geomorphometry.sh [DEM_FILE] [OUTPUT_DIR]
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
OUTPUT_DIR="${2:-outputs/02_geomorphometry}"
```

#### 03_stream_network.sh
```bash
# Usage: ./03_stream_network.sh [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
HYDRO_DIR="${2:-outputs/01_hydrology}"
OUTPUT_DIR="${3:-outputs/03_stream_network}"
```

#### 04_morphometry.sh
```bash
# Usage: ./04_morphometry.sh [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
OUTPUT_DIR="${2:-outputs/04_morphometry}"
GEOMORPH_DIR="${3:-outputs/02_geomorphometry}"
```

#### run_all_workflows.sh
```bash
# Usage: ./run_all_workflows.sh [DEM_FILE]
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
```

### 4. No Input Validation
**Problem**: Scripts would fail with cryptic errors if DEM didn't exist.

**Solution**: Added DEM existence checks to all scripts:
```bash
if [ ! -f "$DEM" ]; then
  echo "ERROR: DEM file not found: $DEM"
  echo "Usage: $0 [DEM_FILE] [OUTPUT_DIR]"
  echo "Example: $0 mydem.tif outputs/01_hydrology"
  exit 1
fi
```

---

## Updated Usage

### Default Usage (Dettelbach DEM)
```bash
# Use default DEM (DEM5_bbox_Dettelbach.tif)
./01_hydrology.sh
./02_geomorphometry.sh
./03_stream_network.sh
./04_morphometry.sh
```

### Custom DEM Usage
```bash
# Use a different DEM
./01_hydrology.sh my_custom_dem.tif

# Or specify custom output directory too
./01_hydrology.sh my_custom_dem.tif outputs/my_hydrology

# For stream network (needs hydrology outputs)
./03_stream_network.sh my_custom_dem.tif outputs/my_hydrology outputs/my_streams
```

### Master Script
```bash
# Default DEM
./run_all_workflows.sh

# Custom DEM
./run_all_workflows.sh my_custom_dem.tif
```

### Python Wrapper (already supported)
```bash
# Default DEM
./run_workflows.py --all

# Custom DEM
./run_workflows.py --all --dem my_custom_dem.tif

# Parallel execution with custom DEM
./run_workflows.py --parallel --dem my_custom_dem.tif
```

---

## Testing the Fixes

### Test 1: Run Hydrology with Default DEM
```bash
./01_hydrology.sh
```
**Expected**: Should complete without Hillslopes panic error.

### Test 2: Run with Custom DEM
```bash
# Create a test with your custom DEM
./01_hydrology.sh /path/to/your/dem.tif outputs/test_hydrology
```

### Test 3: Verify Outputs
```bash
# Check that streams were extracted
ls -lh outputs/01_hydrology/streams_temp.tif

# Check that hillslopes completed
ls -lh outputs/01_hydrology/hillslopes.tif

# Check that subbasins completed
ls -lh outputs/01_hydrology/subbasins.tif
```

### Test 4: Run All Workflows
```bash
# Clean previous outputs
rm -rf outputs/

# Run all workflows
./run_all_workflows.sh

# Verify no errors
echo $?  # Should be 0
```

---

## Files Modified

1. `01_hydrology.sh` - Fixed Hillslopes/Subbasins, added CLI args
2. `02_geomorphometry.sh` - Added CLI args
3. `03_stream_network.sh` - Added CLI args
4. `04_morphometry.sh` - Added CLI args
5. `run_all_workflows.sh` - Added CLI args, passes DEM to workflows

---

## Changes Summary

### In 01_hydrology.sh

**Section 4: Watershed Delineation** (Lines ~132-162)
- Added `ExtractStreams` before Hillslopes/Subbasins
- Updated Hillslopes to use `--streams="$OUTPUT_DIR/streams_temp.tif"`
- Updated Subbasins to use `--streams="$OUTPUT_DIR/streams_temp.tif"`

**Section 5: Stream-Related Metrics** (Lines ~165-182)
- Updated ElevationAboveStream to use extracted streams
- Updated DownslopeDistanceToStream to use extracted streams

**Header** (Lines 1-28)
- Added command-line argument parsing
- Added DEM existence validation
- Added usage instructions

---

## Key Tool Requirements (Learned)

### Tools that need EXTRACTED STREAMS (not flow accumulation):
- `Hillslopes` - needs `--streams` parameter with extracted streams
- `Subbasins` - needs `--streams` parameter with extracted streams
- `ElevationAboveStream` - needs `--streams` parameter with extracted streams
- `DownslopeDistanceToStream` - needs `--streams` parameter with extracted streams

### How to extract streams:
```bash
whitebox_tools -r=ExtractStreams \
  --flow_accum="flow_accumulation.tif" \
  -o="streams.tif" \
  --threshold=1000  # Adjust based on DEM resolution and area size
```

---

## Notes

- The stream threshold (1000 cells) is a reasonable default but may need adjustment based on:
  - DEM resolution (higher resolution = higher threshold)
  - Study area size
  - Desired stream density

- All scripts now have **backward compatibility** - they work with or without arguments

- The Python wrapper (`run_workflows.py`) already had DEM argument support via `--dem` flag

---

## If You Still Get Errors

1. **Check WhiteboxTools version**:
   ```bash
   whitebox_tools --version
   ```

2. **Test individual tools**:
   ```bash
   whitebox_tools --toolhelp=Hillslopes
   whitebox_tools --toolhelp=ExtractStreams
   ```

3. **Check input DEM**:
   ```bash
   gdalinfo DEM5_bbox_Dettelbach.tif
   ```

4. **View logs**:
   ```bash
   tail -100 logs/01_hydrology_*.log
   ```

5. **Run with verbose output**:
   ```bash
   bash -x ./01_hydrology.sh 2>&1 | tee debug.log
   ```
