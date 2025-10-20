#!/bin/bash

# ============================================================================
# MORPHOMETRY AND TERRAIN ANALYSIS WORKFLOW
# Advanced morphometric and terrain analysis using WhiteboxTools
# Usage: ./04_morphometry.sh [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]
# ============================================================================

# Configuration - use command-line args or defaults
DEM="${1:-dem.tif}"
OUTPUT_DIR="${2:-outputs/04_morphometry}"
GEOMORPH_DIR="${3:-outputs/02_geomorphometry}"

# Check if DEM exists
if [ ! -f "$DEM" ]; then
  echo "ERROR: DEM file not found: $DEM"
  echo "Usage: $0 [DEM_FILE] [OUTPUT_DIR] [GEOMORPH_DIR]"
  echo "Example: $0 mydem.tif outputs/04_morphometry outputs/02_geomorphometry"
  exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "MORPHOMETRY WORKFLOW STARTED"
echo "Input DEM: $DEM"
echo "Output Directory: $OUTPUT_DIR"
echo "========================================"

# ============================================================================
# 1. ELEVATION DERIVATIVES
# ============================================================================
echo ""
echo "[1/10] Elevation Derivatives..."

# Elevation above sea level statistics
echo "  - Calculating elevation statistics..."
whitebox_tools --wd=. -r=RasterHistogram \
  --input="$DEM" \
  -o="$OUTPUT_DIR/elevation_histogram.html"

# Standard deviation of elevation
echo "  - Calculating standard deviation of elevation..."
whitebox_tools --wd=. -r=StdDevFilter \
  --input="$DEM" \
  -o="$OUTPUT_DIR/elevation_stddev.tif" \
  --filterx=11 \
  --filtery=11

# Range of elevation
echo "  - Calculating elevation range..."
whitebox_tools --wd=. -r=RangeFilter \
  --input="$DEM" \
  -o="$OUTPUT_DIR/elevation_range.tif" \
  --filterx=11 \
  --filtery=11

# ============================================================================
# 2. SLOPE DERIVATIVES
# ============================================================================
echo ""
echo "[2/10] Slope Derivatives..."

# Check if geomorphometry outputs exist, otherwise create slope
if [ ! -f "$GEOMORPH_DIR/slope_degrees.tif" ]; then
  echo "  - Creating slope (degrees)..."
  whitebox_tools --wd=. -r=Slope \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/slope_degrees.tif" \
    --units=degrees
  SLOPE_FILE="$OUTPUT_DIR/slope_degrees.tif"
else
  SLOPE_FILE="$GEOMORPH_DIR/slope_degrees.tif"
fi

# Slope standard deviation
echo "  - Calculating slope standard deviation..."
whitebox_tools --wd=. -r=StdDevFilter \
  --input="$SLOPE_FILE" \
  -o="$OUTPUT_DIR/slope_stddev.tif" \
  --filterx=11 \
  --filtery=11

# Slope range
echo "  - Calculating slope range..."
whitebox_tools --wd=. -r=RangeFilter \
  --input="$SLOPE_FILE" \
  -o="$OUTPUT_DIR/slope_range.tif" \
  --filterx=11 \
  --filtery=11

# ============================================================================
# 3. TERRAIN TEXTURE AND PATTERN
# ============================================================================
echo ""
echo "[3/10] Terrain Texture and Pattern..."

# Edge density
echo "  - Calculating edge density..."
whitebox_tools --wd=. -r=EdgeDensity \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/edge_density.tif"

# Embankment mapping
echo "  - Mapping embankments..."
whitebox_tools --wd=. -r=EmbankmentMapping \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/embankments.tif" \
  --road_vec="none" 2>/dev/null || echo "    (Skipped - requires road vector)"

# ============================================================================
# 4. FEATURE PRESERVATION SMOOTHING
# ============================================================================
echo ""
echo "[4/10] Feature Preservation Smoothing..."

# Feature preserving smoothing
echo "  - Applying feature preserving smoothing..."
whitebox_tools --wd=. -r=FeaturePreservingSmoothing \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/dem_smoothed.tif" \
  --filter=11

# Gaussian filter
echo "  - Applying Gaussian filter..."
whitebox_tools --wd=. -r=GaussianFilter \
  --input="$DEM" \
  -o="$OUTPUT_DIR/dem_gaussian.tif" \
  --sigma=1.5

# Mean filter
echo "  - Applying mean filter..."
whitebox_tools --wd=. -r=MeanFilter \
  --input="$DEM" \
  -o="$OUTPUT_DIR/dem_mean_filtered.tif" \
  --filterx=5 \
  --filtery=5

# Median filter
echo "  - Applying median filter..."
whitebox_tools --wd=. -r=MedianFilter \
  --input="$DEM" \
  -o="$OUTPUT_DIR/dem_median_filtered.tif" \
  --filterx=5 \
  --filtery=5

# ============================================================================
# 5. RELATIVE TOPOGRAPHIC POSITION
# ============================================================================
echo ""
echo "[5/10] Relative Topographic Position..."

# Relative topographic position at multiple scales
echo "  - Calculating relative topographic position (multiple scales)..."
for scale in 3 5 11 21 51; do
  echo "    Scale: ${scale}x${scale} cells"
  whitebox_tools --wd=. -r=DevFromMeanElev \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/rel_topo_pos_${scale}x${scale}.tif" \
    --filterx=$scale \
    --filtery=$scale
done

# ============================================================================
# 6. DOWNSLOPE INDEX
# ============================================================================
echo ""
echo "[6/10] Downslope Index..."

# Downslope index
echo "  - Calculating downslope index..."
whitebox_tools --wd=. -r=DownslopeIndex \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/downslope_index.tif"

# ============================================================================
# 7. MULTISCALE TOPOGRAPHIC METRICS
# ============================================================================
echo ""
echo "[7/10] Multiscale Topographic Metrics..."

# Multiscale elevation percentile
echo "  - Calculating multiscale elevation percentile..."
for scale in 5 10 20; do
  echo "    Scale: ${scale} cells radius"
  filter_size=$((scale * 2 + 1))
  whitebox_tools --wd=. -r=ElevPercentile \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/elev_percentile_scale${scale}.tif" \
    --filterx=$filter_size \
    --filtery=$filter_size
done

# ============================================================================
# 8. ASPECT-BASED MORPHOMETRY
# ============================================================================
echo ""
echo "[8/10] Aspect-Based Morphometry..."

# Aspect if not exists
if [ ! -f "$GEOMORPH_DIR/aspect.tif" ]; then
  echo "  - Creating aspect..."
  whitebox_tools --wd=. -r=Aspect \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/aspect.tif"
  ASPECT_FILE="$OUTPUT_DIR/aspect.tif"
else
  ASPECT_FILE="$GEOMORPH_DIR/aspect.tif"
fi

# Linear aspect
echo "  - Calculating linear aspect..."
whitebox_tools --wd=. -r=Aspect \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/aspect_linear.tif"

# ============================================================================
# 9. PROFILE AND TANGENTIAL CURVATURE COMBINATIONS
# ============================================================================
echo ""
echo "[9/10] Profile and Tangential Curvature Combinations..."

# Profile curvature if not exists
if [ ! -f "$GEOMORPH_DIR/profile_curvature.tif" ]; then
  echo "  - Creating profile curvature..."
  whitebox_tools --wd=. -r=ProfileCurvature \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/profile_curvature.tif"
fi

# Plan curvature if not exists
if [ ! -f "$GEOMORPH_DIR/plan_curvature.tif" ]; then
  echo "  - Creating plan curvature..."
  whitebox_tools --wd=. -r=PlanCurvature \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/plan_curvature.tif"
fi

# Note: Unsphericity and ShapeIndex are licensed tools (Whitebox extension)
echo "  - Skipping licensed tools (Unsphericity, ShapeIndex)"

# ============================================================================
# 10. FLOW TOPOLOGY METRICS
# ============================================================================
echo ""
echo "[10/10] Flow Topology Metrics..."

# Max upslope elevation change (free tool)
echo "  - Calculating max upslope elevation change..."
whitebox_tools --wd=. -r=MaxUpslopeElevChange \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/max_upslope_elev_change.tif"

# Number of upslope neighbours (free tool)
echo "  - Calculating number of upslope neighbours..."
whitebox_tools --wd=. -r=NumUpslopeNeighbours \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/num_upslope_neighbours.tif"

# Note: ImpoundmentSizeIndex is a licensed tool (Whitebox extension)
echo "  - Skipping licensed tool (ImpoundmentSizeIndex)"

echo ""
echo "========================================"
echo "MORPHOMETRY WORKFLOW COMPLETED"
echo "Outputs saved to: $OUTPUT_DIR"
echo "========================================"
