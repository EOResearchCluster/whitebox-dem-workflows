# Quick Start Guide

## 1. Run Everything (Easiest)

```bash
./run_all_workflows.sh
```

This runs all 4 workflows in sequence with full logging and colored output.

---

## 2. Run with Python (Parallel Processing)

```bash
# Run independent workflows in parallel (FASTEST)
./run_workflows.py --parallel

# Or run all sequentially
./run_workflows.py --all

# Or run just one workflow
./run_workflows.py --workflow hydrology
```

---

## 3. Run Individual Workflows

```bash
# Independent workflows (can run in any order)
./02_geomorphometry.sh    # Terrain attributes & curvatures
./01_hydrology.sh         # Flow & watersheds
./04_morphometry.sh       # Advanced terrain metrics

# Dependent workflow (run AFTER hydrology)
./03_stream_network.sh    # Stream extraction & analysis
```

---

## 4. Quick Commands

### Load Utility Functions
```bash
# Source utility functions for easy access
source utils.sh

# Now you have access to:
rp <pattern>                    # Quick raster preview
list_outputs                    # List all outputs
workflow_status                 # Check completion
```

### Quick Raster Visualization
```bash
# View any raster quickly
rp slope                        # Finds and displays first "slope" file
rp hillshade                    # Auto-selects gray colormap
rp twi --cmap YlGnBu           # Custom colormap
rp dem --hillshade             # Apply hillshade overlay

# Or use the full script
./view_raster.py outputs/01_hydrology/wetness_index.tif
```

### List Available Workflows
```bash
./run_workflows.py --list
```

### Check WhiteboxTools Installation
```bash
whitebox_tools --version
whitebox_tools --listtools | grep -i slope
```

### View Output Files
```bash
list_outputs                    # All outputs with file counts
list_outputs hydrology          # Specific workflow
```

### Check Status
```bash
workflow_status                 # See which workflows completed
```

### View Logs
```bash
ls -lt logs/
tail -f logs/01_hydrology_*.log  # Follow hydrology log
```

---

## Expected Outputs

### Total Files Generated
- **~150+ GeoTIFF files**
- **~10 vector shapefiles**
- **~5 HTML reports**

### Processing Time
- **Sequential**: 8-21 minutes
- **Parallel**: 5-12 minutes (Python with --parallel)

---

## Output Highlights

### Hydrology
- `outputs/01_hydrology/dem_breached.tif` - Depression-breached DEM
- `outputs/01_hydrology/d8_flow_accum.tif` - Flow accumulation
- `outputs/01_hydrology/basins.tif` - Drainage basins
- `outputs/01_hydrology/wetness_index.tif` - Topographic Wetness Index

### Geomorphometry
- `outputs/02_geomorphometry/slope_degrees.tif` - Slope in degrees
- `outputs/02_geomorphometry/hillshade.tif` - Hillshade visualization
- `outputs/02_geomorphometry/profile_curvature.tif` - Profile curvature
- `outputs/02_geomorphometry/geomorphons.tif` - Landform classification

### Stream Network
- `outputs/03_stream_network/streams_1000.tif` - Extracted streams
- `outputs/03_stream_network/strahler_order.tif` - Strahler stream order
- `outputs/03_stream_network/long_profile.html` - Longitudinal profile plot

### Morphometry
- `outputs/04_morphometry/rel_topo_pos_*.tif` - Topographic position (multi-scale)
- `outputs/04_morphometry/downslope_index.tif` - Downslope index
- `outputs/04_morphometry/edge_density.tif` - Terrain complexity

---

## Troubleshooting

### If a script fails:
```bash
# Check the log file
cat logs/01_hydrology_*.log | tail -50

# Re-run just that workflow
./01_hydrology.sh
```

### If "command not found":
```bash
# Install WhiteboxTools
pixi global install whitebox_tools

# Make scripts executable
chmod +x *.sh *.py
```

### If out of disk space:
```bash
# Check disk usage
du -sh outputs/*/

# Remove outputs and re-run
rm -rf outputs/ logs/
./run_all_workflows.sh
```

---

## Next Steps

1. **View outputs in QGIS**:
   - Drag and drop `.tif` files into QGIS
   - Use appropriate color ramps for visualization
   - Overlay hillshade for better visualization

2. **Further analysis**:
   - Use outputs as inputs for other models
   - Calculate additional derivatives
   - Perform statistical analysis in R/Python

3. **Customize workflows**:
   - Edit `*.sh` scripts to add more analyses
   - Adjust parameters (thresholds, scales, etc.)
   - Add additional WhiteboxTools functions

---

## Resources

- **Full Documentation**: See `README.md`
- **WhiteboxTools Manual**: https://www.whiteboxgeo.com/manual/wbt_book/
- **Tool Help**: `whitebox_tools --toolhelp=ToolName`
