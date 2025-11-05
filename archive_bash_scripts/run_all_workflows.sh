#!/bin/bash

# ============================================================================
# MASTER WORKFLOW SCRIPT
# Runs all WhiteboxTools geoprocessing workflows in sequence
# Usage: ./run_all_workflows.sh [DEM_FILE]
# ============================================================================

# Colors for output (optional, comment out if not supported)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - use command-line arg or default
DEM="${1:-dem.tif}"
LOG_DIR="logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create log directory
mkdir -p "$LOG_DIR"

# Function to print colored status messages
print_status() {
  echo -e "${BLUE}[$(date +"%Y-%m-%d %H:%M:%S")]${NC} $1"
}

print_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Function to run a workflow and log output
run_workflow() {
  local script_name=$1
  local workflow_name=$2
  local log_file="$LOG_DIR/${script_name%.sh}_${TIMESTAMP}.log"

  print_status "Starting $workflow_name..."

  if bash "$script_name" "$DEM" 2>&1 | tee "$log_file"; then
    print_success "$workflow_name completed successfully"
    echo "Log file: $log_file"
    return 0
  else
    print_error "$workflow_name failed!"
    echo "Check log file: $log_file"
    return 1
  fi
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

echo ""
echo "============================================================================"
echo "                    WHITEBOX GEOPROCESSING WORKFLOWS"
echo "============================================================================"
echo ""
echo "Input DEM: $DEM"
echo "Start time: $(date)"
echo "Log directory: $LOG_DIR"
echo ""
echo "This script will run the following workflows:"
echo "  1. Geomorphometry (can run independently)"
echo "  2. Hydrology (can run independently)"
echo "  3. Stream Network Analysis (requires hydrology)"
echo "  4. Morphometry (can run independently)"
echo ""
echo "============================================================================"
echo ""

# Check if DEM exists
if [ ! -f "$DEM" ]; then
  print_error "DEM file not found: $DEM"
  exit 1
fi

# Make scripts executable
chmod +x 01_hydrology.sh 02_geomorphometry.sh 03_stream_network.sh 04_morphometry.sh

# Track overall start time
overall_start=$(date +%s)

# ============================================================================
# WORKFLOW 1: GEOMORPHOMETRY (Independent)
# ============================================================================
echo ""
print_status "═══════════════════════════════════════════════════════════════════════"
print_status "WORKFLOW 1/4: GEOMORPHOMETRY"
print_status "═══════════════════════════════════════════════════════════════════════"
workflow1_start=$(date +%s)

if run_workflow "02_geomorphometry.sh" "Geomorphometry Workflow"; then
  workflow1_end=$(date +%s)
  workflow1_duration=$((workflow1_end - workflow1_start))
  print_success "Geomorphometry completed in ${workflow1_duration} seconds"
else
  print_error "Geomorphometry workflow failed. Continuing with other workflows..."
fi

# ============================================================================
# WORKFLOW 2: HYDROLOGY (Independent)
# ============================================================================
echo ""
print_status "═══════════════════════════════════════════════════════════════════════"
print_status "WORKFLOW 2/4: HYDROLOGY"
print_status "═══════════════════════════════════════════════════════════════════════"
workflow2_start=$(date +%s)

if run_workflow "01_hydrology.sh" "Hydrology Workflow"; then
  workflow2_end=$(date +%s)
  workflow2_duration=$((workflow2_end - workflow2_start))
  print_success "Hydrology completed in ${workflow2_duration} seconds"
  hydrology_success=true
else
  print_error "Hydrology workflow failed. Stream network analysis will be skipped."
  hydrology_success=false
fi

# ============================================================================
# WORKFLOW 3: STREAM NETWORK ANALYSIS (Depends on Hydrology)
# ============================================================================
echo ""
print_status "═══════════════════════════════════════════════════════════════════════"
print_status "WORKFLOW 3/4: STREAM NETWORK ANALYSIS"
print_status "═══════════════════════════════════════════════════════════════════════"

if [ "$hydrology_success" = true ]; then
  workflow3_start=$(date +%s)

  if run_workflow "03_stream_network.sh" "Stream Network Analysis Workflow"; then
    workflow3_end=$(date +%s)
    workflow3_duration=$((workflow3_end - workflow3_start))
    print_success "Stream Network Analysis completed in ${workflow3_duration} seconds"
  else
    print_error "Stream Network Analysis workflow failed."
  fi
else
  print_warning "Skipping Stream Network Analysis (requires hydrology outputs)"
fi

# ============================================================================
# WORKFLOW 4: MORPHOMETRY (Independent, but benefits from geomorphometry)
# ============================================================================
echo ""
print_status "═══════════════════════════════════════════════════════════════════════"
print_status "WORKFLOW 4/4: MORPHOMETRY"
print_status "═══════════════════════════════════════════════════════════════════════"
workflow4_start=$(date +%s)

if run_workflow "04_morphometry.sh" "Morphometry Workflow"; then
  workflow4_end=$(date +%s)
  workflow4_duration=$((workflow4_end - workflow4_start))
  print_success "Morphometry completed in ${workflow4_duration} seconds"
else
  print_error "Morphometry workflow failed."
fi

# ============================================================================
# SUMMARY
# ============================================================================
overall_end=$(date +%s)
overall_duration=$((overall_end - overall_start))

echo ""
echo "============================================================================"
echo "                           PROCESSING COMPLETE"
echo "============================================================================"
echo ""
echo "Total execution time: ${overall_duration} seconds ($((overall_duration / 60)) minutes)"
echo "End time: $(date)"
echo ""
echo "Output directories:"
echo "  - outputs/01_hydrology/"
echo "  - outputs/02_geomorphometry/"
echo "  - outputs/03_stream_network/"
echo "  - outputs/04_morphometry/"
echo ""
echo "Log files saved to: $LOG_DIR/"
echo ""
echo "============================================================================"
echo ""

# Generate summary statistics
echo "Generating output summary..."
echo ""
echo "File counts per workflow:"
echo "  Hydrology:        $(find outputs/01_hydrology -type f 2>/dev/null | wc -l || echo 0) files"
echo "  Geomorphometry:   $(find outputs/02_geomorphometry -type f 2>/dev/null | wc -l || echo 0) files"
echo "  Stream Network:   $(find outputs/03_stream_network -type f 2>/dev/null | wc -l || echo 0) files"
echo "  Morphometry:      $(find outputs/04_morphometry -type f 2>/dev/null | wc -l || echo 0) files"
echo ""

print_success "All workflows completed! Check the outputs/ directory for results."
