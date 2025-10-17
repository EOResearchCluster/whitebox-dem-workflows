#!/bin/bash

# ============================================================================
# STREAM NETWORK ANALYSIS WORKFLOW
# Comprehensive stream network analysis using WhiteboxTools
# Usage: ./03_stream_network.sh [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]
# Prerequisites: Requires outputs from 01_hydrology.sh
# ============================================================================

# Configuration - use command-line args or defaults
DEM="${1:-DEM5_bbox_Dettelbach.tif}"
HYDRO_DIR="${2:-outputs/01_hydrology}"
OUTPUT_DIR="${3:-outputs/03_stream_network}"

# Check if DEM exists
if [ ! -f "$DEM" ]; then
  echo "ERROR: DEM file not found: $DEM"
  echo "Usage: $0 [DEM_FILE] [HYDRO_DIR] [OUTPUT_DIR]"
  echo "Example: $0 mydem.tif outputs/01_hydrology outputs/03_stream_network"
  exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "STREAM NETWORK ANALYSIS STARTED"
echo "Input DEM: $DEM"
echo "Hydrology Directory: $HYDRO_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "========================================"

# Check if hydrology outputs exist
if [ ! -f "$HYDRO_DIR/d8_pointer.tif" ]; then
  echo "ERROR: Hydrology workflow must be run first!"
  echo "Run: bash 01_hydrology.sh"
  exit 1
fi

# ============================================================================
# 1. STREAM EXTRACTION
# ============================================================================
echo ""
echo "[1/8] Stream Extraction..."

# Extract streams using different thresholds
echo "  - Extracting streams (threshold: 1000 cells)..."
whitebox_tools -r=ExtractStreams \
  --flow_accum="$HYDRO_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/streams_1000.tif" \
  --threshold=1000

echo "  - Extracting streams (threshold: 500 cells)..."
whitebox_tools -r=ExtractStreams \
  --flow_accum="$HYDRO_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/streams_500.tif" \
  --threshold=500

echo "  - Extracting streams (threshold: 2000 cells)..."
whitebox_tools -r=ExtractStreams \
  --flow_accum="$HYDRO_DIR/d8_flow_accum.tif" \
  -o="$OUTPUT_DIR/streams_2000.tif" \
  --threshold=2000

# Extract valleys
echo "  - Extracting valleys..."
whitebox_tools -r=ExtractValleys \
  --dem="$HYDRO_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/valleys.tif"

# ============================================================================
# 2. STREAM VECTORIZATION
# ============================================================================
echo ""
echo "[2/8] Stream Vectorization..."

# Convert raster streams to vector
echo "  - Converting raster streams to vector (1000 threshold)..."
whitebox_tools -r=RasterStreamsToVector \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/streams_1000_vector.shp"

echo "  - Converting raster streams to vector (500 threshold)..."
whitebox_tools -r=RasterStreamsToVector \
  --streams="$OUTPUT_DIR/streams_500.tif" \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  -o="$OUTPUT_DIR/streams_500_vector.shp"

# ============================================================================
# 3. STREAM ORDERING
# ============================================================================
echo ""
echo "[3/8] Stream Ordering Systems..."

# Strahler stream order
echo "  - Calculating Strahler stream order..."
whitebox_tools -r=StrahlerStreamOrder \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/strahler_order.tif"

# Horton stream order
echo "  - Calculating Horton stream order..."
whitebox_tools -r=HortonStreamOrder \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/horton_order.tif"

# Shreve stream magnitude
echo "  - Calculating Shreve stream magnitude..."
whitebox_tools -r=ShreveStreamMagnitude \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/shreve_magnitude.tif"

# Hack stream order
echo "  - Calculating Hack stream order..."
whitebox_tools -r=HackStreamOrder \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/hack_order.tif"

# Topological stream order
echo "  - Calculating topological stream order..."
whitebox_tools -r=TopologicalStreamOrder \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/topological_order.tif"

# ============================================================================
# 4. STREAM LINK ANALYSIS
# ============================================================================
echo ""
echo "[4/8] Stream Link Analysis..."

# Stream link identifier
echo "  - Identifying stream links..."
whitebox_tools -r=StreamLinkIdentifier \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/stream_links.tif"

# Stream link length
echo "  - Calculating stream link lengths..."
whitebox_tools -r=StreamLinkLength \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --linkid="$OUTPUT_DIR/stream_links.tif" \
  -o="$OUTPUT_DIR/stream_link_length.tif"

# Stream link slope
echo "  - Calculating stream link slopes..."
whitebox_tools -r=StreamLinkSlope \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --linkid="$OUTPUT_DIR/stream_links.tif" \
  --dem="$HYDRO_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/stream_link_slope.tif"

# Stream link class
echo "  - Classifying stream links..."
whitebox_tools -r=StreamLinkClass \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/stream_link_class.tif"

# ============================================================================
# 5. TRIBUTARY ANALYSIS
# ============================================================================
echo ""
echo "[5/8] Tributary Analysis..."

# Tributary identifier
echo "  - Identifying tributaries..."
whitebox_tools -r=TributaryIdentifier \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/tributaries.tif"

# ============================================================================
# 6. CHANNEL HEAD AND NETWORK METRICS
# ============================================================================
echo ""
echo "[6/8] Channel Head and Network Metrics..."

# Farthest channel head
echo "  - Calculating distance to farthest channel head..."
whitebox_tools -r=FarthestChannelHead \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/farthest_channel_head.tif"

# Length of upstream channels
echo "  - Calculating length of upstream channels..."
whitebox_tools -r=LengthOfUpstreamChannels \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/upstream_channel_length.tif"

# Distance to outlet
echo "  - Calculating distance to outlet..."
whitebox_tools -r=DistanceToOutlet \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/distance_to_outlet.tif"

# ============================================================================
# 7. MAIN STEM IDENTIFICATION
# ============================================================================
echo ""
echo "[7/8] Main Stem Identification..."

# Find main stem
echo "  - Finding main stem..."
whitebox_tools -r=FindMainStem \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/main_stem.tif"

# ============================================================================
# 8. LONGITUDINAL PROFILES
# ============================================================================
echo ""
echo "[8/8] Longitudinal Profiles..."

# Long profile
echo "  - Creating longitudinal stream profile..."
whitebox_tools -r=LongProfile \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  --dem="$HYDRO_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/long_profile.html"

# Stream slope (continuous)
echo "  - Calculating continuous stream slope..."
whitebox_tools -r=StreamSlopeContinuous \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  --dem="$HYDRO_DIR/dem_breached.tif" \
  -o="$OUTPUT_DIR/stream_slope_continuous.tif"

# Remove short streams (creating cleaned network)
echo "  - Removing short streams (<100m)..."
whitebox_tools -r=RemoveShortStreams \
  --d8_pntr="$HYDRO_DIR/d8_pointer.tif" \
  --streams="$OUTPUT_DIR/streams_1000.tif" \
  -o="$OUTPUT_DIR/streams_cleaned.tif" \
  --min_length=100.0

echo ""
echo "========================================"
echo "STREAM NETWORK ANALYSIS COMPLETED"
echo "Outputs saved to: $OUTPUT_DIR"
echo "========================================"
