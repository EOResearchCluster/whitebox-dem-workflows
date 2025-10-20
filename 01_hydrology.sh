#!/bin/bash

# ============================================================================
# HYDROLOGY WORKFLOW
# Comprehensive hydrological analysis using WhiteboxTools
# Usage: ./01_hydrology.sh [DEM_FILE] [OUTPUT_DIR]
# ============================================================================

# Configuration - use command-line args or defaults
DEM="${1:-dem.tif}"
OUTPUT_DIR="${2:-outputs/01_hydrology}"

# Check if DEM exists
if [ ! -f "$DEM" ]; then
  echo "ERROR: DEM file not found: $DEM"
  echo "Usage: $0 [DEM_FILE] [OUTPUT_DIR]"
  echo "Example: $0 mydem.tif outputs/01_hydrology"
  exit 1
fi

# Create output directory
install -d -D "$OUTPUT_DIR"

echo "========================================"
echo "HYDROLOGY WORKFLOW STARTED"
echo "Input DEM: $DEM"
echo "Output Directory: $OUTPUT_DIR"
echo "========================================"

# ============================================================================
# 1. DEPRESSION HANDLING
# ============================================================================
echo ""
echo "[1/9] Depression Handling..."

# Breach depressions (preferred method)
echo "  - Breaching depressions (Lindsay 2016 algorithm)..."
whitebox_tools --wd=. -r=BreachDepressions \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/dem_breached.tif"

# Breach depressions using least-cost method
echo "  - Breaching depressions (least-cost method)..."
whitebox_tools --wd=. -r=BreachDepressionsLeastCost \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/dem_breached_leastcost.tif"

# Fill depressions (alternative method)
echo "  - Filling depressions..."
whitebox_tools --wd=. -r=FillDepressions \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/dem_filled.tif"

# Fill single-cell pits
echo "  - Filling single-cell pits..."
whitebox_tools --wd=. -r=FillSingleCellPits \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/dem_pits_filled.tif"

# Depth in sink
echo "  - Calculating depth in sinks..."
whitebox_tools --wd=. -r=DepthInSink \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/depth_in_sink.tif"

# ============================================================================
# 2. FLOW DIRECTION (Using breached DEM)
# ============================================================================
echo ""
echo "[2/9] Flow Direction Analysis..."

# D8 flow pointer
echo "  - D8 flow pointer..."
whitebox_tools --wd=. -r=D8Pointer \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/d8_pointer.tif"

# D-infinity flow pointer
echo "  - D-infinity flow pointer..."
whitebox_tools --wd=. -r=DInfPointer \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/dinf_pointer.tif"

# FD8 flow pointer
echo "  - FD8 flow pointer..."
whitebox_tools --wd=. -r=Fd8Pointer \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/fd8_pointer.tif"

# ============================================================================
# 3. FLOW ACCUMULATION
# ============================================================================
echo ""
echo "[3/9] Flow Accumulation Analysis..."

# D8 flow accumulation
echo "  - D8 flow accumulation..."
whitebox_tools --wd=. -r=D8FlowAccumulation \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/d8_flow_accum.tif" \
  --out_type=cells

# D8 flow accumulation (specific catchment area)
echo "  - D8 flow accumulation (specific catchment area)..."
whitebox_tools --wd=. -r=D8FlowAccumulation \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/d8_flow_accum_sca.tif" \
  --out_type=sca

# D-infinity flow accumulation
echo "  - D-infinity flow accumulation..."
whitebox_tools --wd=. -r=DInfFlowAccumulation \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/dinf_flow_accum.tif" \
  --out_type=cells

# D-infinity flow accumulation (specific catchment area)
echo "  - D-infinity flow accumulation (specific catchment area)..."
whitebox_tools --wd=. -r=DInfFlowAccumulation \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/dinf_flow_accum_sca.tif" \
  --out_type=sca

# FD8 flow accumulation
echo "  - FD8 flow accumulation..."
whitebox_tools --wd=. -r=Fd8FlowAccumulation \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/fd8_flow_accum.tif" \
  --out_type=cells

# ============================================================================
# 4. WATERSHED DELINEATION
# ============================================================================
echo ""
echo "[4/9] Watershed Delineation..."

# First extract streams (needed for hillslopes and subbasins)
echo "  - Extracting streams for watershed analysis..."
whitebox_tools --wd=. -r=ExtractStreams \
  --flow_accum="$OUTPUT_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/streams_temp.tif" \
  --threshold=1000

# Drainage basins
echo "  - Extracting drainage basins..."
whitebox_tools --wd=. -r=Basins \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/basins.tif"

# Hillslopes (requires streams raster)
echo "  - Extracting hillslopes..."
whitebox_tools --wd=. -r=Hillslopes \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \
  -o="$OUTPUT_DIR/hillslopes.tif"

# Subbasins (requires streams raster)
echo "  - Extracting subbasins..."
whitebox_tools --wd=. -r=Subbasins \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \
  -o="$OUTPUT_DIR/subbasins.tif"

# ============================================================================
# 5. STREAM-RELATED METRICS
# ============================================================================
echo ""
echo "[5/9] Stream-Related Metrics..."

# Elevation above stream (uses extracted streams)
echo "  - Calculating elevation above stream..."
whitebox_tools --wd=. -r=ElevationAboveStream \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \
  -o="$OUTPUT_DIR/elevation_above_stream.tif"

# Downslope distance to stream (uses extracted streams)
echo "  - Calculating downslope distance to stream..."
whitebox_tools --wd=. -r=DownslopeDistanceToStream \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  --streams="$OUTPUT_DIR/streams_temp.tif" \
  -o="$OUTPUT_DIR/distance_to_stream.tif"

# ============================================================================
# 6. FLOWPATH ANALYSIS
# ============================================================================
echo ""
echo "[6/9] Flowpath Analysis..."

# Average upslope flowpath length
echo "  - Calculating average upslope flowpath length..."
whitebox_tools --wd=. -r=AverageUpslopeFlowpathLength \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/avg_upslope_flowpath_length.tif"

# Average flowpath slope
echo "  - Calculating average flowpath slope..."
whitebox_tools --wd=. -r=AverageFlowpathSlope \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/avg_flowpath_slope.tif"

# Downslope flowpath length
echo "  - Calculating downslope flowpath length..."
whitebox_tools --wd=. -r=DownslopeFlowpathLength \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/downslope_flowpath_length.tif"

# Maximum upslope flowpath length
echo "  - Calculating maximum upslope flowpath length..."
whitebox_tools --wd=. -r=MaxUpslopeFlowpathLength \
  --d8_pntr="$OUTPUT_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/max_upslope_flowpath_length.tif"

# ============================================================================
# 7. TOPOGRAPHIC WETNESS
# ============================================================================
echo ""
echo "[7/9] Topographic Wetness Indices..."

# Topographic wetness index (TWI)
echo "  - Calculating topographic wetness index (TWI)..."
whitebox_tools --wd=. -r=WetnessIndex \
  --sca="$OUTPUT_DIR/d8_flow_accum_sca.tif" \
  --slope="outputs/02_geomorphometry/slope_degrees.tif" \
  -o="$OUTPUT_DIR/wetness_index.tif" 2>/dev/null || echo "    (Skipped - requires slope from geomorphometry)"

# ============================================================================
# 8. STREAM POWER AND EROSION INDICES
# ============================================================================
echo ""
echo "[8/9] Stream Power and Erosion Indices..."

# Stream power index
echo "  - Calculating stream power index..."
whitebox_tools --wd=. -r=StreamPowerIndex \
  --sca="$OUTPUT_DIR/d8_flow_accum_sca.tif" \
  --slope="outputs/02_geomorphometry/slope_degrees.tif" \
  -o="$OUTPUT_DIR/stream_power_index.tif" \
  --exponent=1.0 2>/dev/null || echo "    (Skipped - requires slope from geomorphometry)"

# Sediment transport index
echo "  - Calculating sediment transport index..."
whitebox_tools --wd=. -r=SedimentTransportIndex \
  --sca="$OUTPUT_DIR/d8_flow_accum_sca.tif" \
  --slope="outputs/02_geomorphometry/slope_degrees.tif" \
  -o="$OUTPUT_DIR/sediment_transport_index.tif" \
  --exponent=1.0 2>/dev/null || echo "    (Skipped - requires slope from geomorphometry)"

# ============================================================================
# 9. UTILITY ANALYSES
# ============================================================================
echo ""
echo "[9/9] Utility Analyses..."

# Find no-flow cells
echo "  - Finding no-flow cells..."
whitebox_tools --wd=. -r=FindNoFlowCells \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/no_flow_cells.tif"

# Edge contamination
echo "  - Detecting edge contamination..."
whitebox_tools --wd=. -r=EdgeContamination \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  --flow_accum="$OUTPUT_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/edge_contamination.tif"

# Elevation above pit
echo "  - Calculating elevation above pit..."
whitebox_tools --wd=. -r=ElevAbovePit \
  --dem="$OUTPUT_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/elev_above_pit.tif"

echo ""
echo "========================================"
echo "HYDROLOGY WORKFLOW COMPLETED"
echo "Outputs saved to: $OUTPUT_DIR"
echo "========================================"
