#!/bin/bash

# ============================================================================
# GEOMORPHOMETRY WORKFLOW
# Comprehensive geomorphometric analysis using WhiteboxTools
# Usage: ./02_geomorphometry.sh [DEM_FILE] [OUTPUT_DIR]
# ============================================================================

# Configuration - use command-line args or defaults
DEM="${1:-dem.tif}"
OUTPUT_DIR="${2:-outputs/02_geomorphometry}"

# Check if DEM exists
if [ ! -f "$DEM" ]; then
  echo "ERROR: DEM file not found: $DEM"
  echo "Usage: $0 [DEM_FILE] [OUTPUT_DIR]"
  echo "Example: $0 mydem.tif outputs/02_geomorphometry"
  exit 1
fi

# Create output directory
install -d -D "$OUTPUT_DIR"

echo "========================================"
echo "GEOMORPHOMETRY WORKFLOW STARTED"
echo "Input DEM: $DEM"
echo "Output Directory: $OUTPUT_DIR"
echo "========================================"

# ============================================================================
# 1. BASIC TERRAIN ATTRIBUTES
# ============================================================================
echo ""
echo "[1/12] Basic Terrain Attributes..."

# Slope (multiple units)
echo "  - Calculating slope (degrees)..."
whitebox_tools --wd=. -r=Slope \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/slope_degrees.tif" \
  --units=degrees

echo "  - Calculating slope (radians)..."
whitebox_tools --wd=. -r=Slope \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/slope_radians.tif" \
  --units=radians

echo "  - Calculating slope (percent)..."
whitebox_tools --wd=. -r=Slope \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/slope_percent.tif" \
  --units=percent

# Aspect
echo "  - Calculating aspect..."
whitebox_tools --wd=. -r=Aspect \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/aspect.tif"

# Hillshade
echo "  - Creating hillshade..."
whitebox_tools --wd=. -r=Hillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade.tif" \
  --azimuth=315.0 \
  --altitude=45.0

# Multidirectional hillshade
echo "  - Creating multidirectional hillshade..."
whitebox_tools --wd=. -r=MultidirectionalHillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade_multidirectional.tif"

# ============================================================================
# 2. CURVATURE ANALYSIS
# ============================================================================
echo ""
echo "[2/12] Curvature Analysis..."

# Profile curvature
echo "  - Calculating profile curvature..."
whitebox_tools --wd=. -r=ProfileCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/profile_curvature.tif"

# Plan curvature
echo "  - Calculating plan curvature..."
whitebox_tools --wd=. -r=PlanCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/plan_curvature.tif"

# Tangential curvature
echo "  - Calculating tangential curvature..."
whitebox_tools --wd=. -r=TangentialCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/tangential_curvature.tif"

# Total curvature
echo "  - Calculating total curvature..."
whitebox_tools --wd=. -r=TotalCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/total_curvature.tif"

# Mean curvature
echo "  - Calculating mean curvature..."
whitebox_tools --wd=. -r=MeanCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/mean_curvature.tif"

# Gaussian curvature
echo "  - Calculating Gaussian curvature..."
whitebox_tools --wd=. -r=GaussianCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/gaussian_curvature.tif"

# Minimal curvature
echo "  - Calculating minimal curvature..."
whitebox_tools --wd=. -r=MinimalCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/minimal_curvature.tif"

# Maximal curvature
echo "  - Calculating maximal curvature..."
whitebox_tools --wd=. -r=MaximalCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/maximal_curvature.tif"

# ============================================================================
# 3. ADVANCED CURVATURE METRICS
# ============================================================================
echo ""
echo "[3/12] Advanced Curvature Metrics..."

# Difference curvature
echo "  - Calculating difference curvature..."
whitebox_tools --wd=. -r=DifferenceCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/difference_curvature.tif"

# Horizontal excess curvature
echo "  - Calculating horizontal excess curvature..."
whitebox_tools --wd=. -r=HorizontalExcessCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/horizontal_excess_curvature.tif"

# Vertical excess curvature
echo "  - Calculating vertical excess curvature..."
whitebox_tools --wd=. -r=VerticalExcessCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/vertical_excess_curvature.tif"

# Ring curvature
echo "  - Calculating ring curvature..."
whitebox_tools --wd=. -r=RingCurvature \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/ring_curvature.tif"

# Rotor
echo "  - Calculating rotor..."
whitebox_tools --wd=. -r=Rotor \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/rotor.tif"

# ============================================================================
# 4. SURFACE ROUGHNESS AND TEXTURE
# ============================================================================
echo ""
echo "[4/12] Surface Roughness and Texture..."

# Ruggedness index
echo "  - Calculating terrain ruggedness index (TRI)..."
whitebox_tools --wd=. -r=RuggednessIndex \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/ruggedness_index.tif"

# Multiscale roughness
echo "  - Calculating multiscale roughness..."
whitebox_tools --wd=. -r=MultiscaleRoughness \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/multiscale_roughness.tif"

# Surface area ratio
echo "  - Calculating surface area ratio..."
whitebox_tools --wd=. -r=SurfaceAreaRatio \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/surface_area_ratio.tif"

# Circular variance of aspect
echo "  - Calculating circular variance of aspect..."
whitebox_tools --wd=. -r=CircularVarianceOfAspect \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/circular_variance_aspect.tif"

# Average normal vector angular deviation
echo "  - Calculating average normal vector angular deviation..."
whitebox_tools --wd=. -r=AverageNormalVectorAngularDeviation \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/avg_normal_vector_angular_dev.tif"

# ============================================================================
# 5. SLOPE POSITION AND CLASSIFICATION
# ============================================================================
echo ""
echo "[5/12] Slope Position and Classification..."

# Slope vs elevation percentile
echo "  - Calculating slope vs elevation percentile..."
whitebox_tools --wd=. -r=SlopeVsElevationPlot \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/slope_vs_elevation.html"

# Topographic position index (TPI)
echo "  - Calculating topographic position index (TPI)..."
whitebox_tools --wd=. -r=DevFromMeanElev \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/tpi.tif" \
  --filterx=11 \
  --filtery=11

# Difference from mean elevation
echo "  - Calculating difference from mean elevation..."
whitebox_tools --wd=. -r=DiffFromMeanElev \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/diff_from_mean_elev.tif" \
  --filterx=11 \
  --filtery=11

# Elevation percentile
echo "  - Calculating elevation percentile..."
whitebox_tools --wd=. -r=ElevPercentile \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/elev_percentile.tif" \
  --filterx=11 \
  --filtery=11

# ============================================================================
# 6. RELIEF AND RESIDUALS
# ============================================================================
echo ""
echo "[6/12] Relief and Residuals..."

# Local relief
echo "  - Calculating local relief (multiple scales)..."
for radius in 5 10 20 50; do
  echo "    Scale: ${radius} cells"
  whitebox_tools --wd=. -r=MaxElevationDeviation \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/relief_${radius}cell.tif" \
    --filterx=$((radius * 2 + 1)) \
    --filtery=$((radius * 2 + 1))
done

# Directional relief
echo "  - Calculating directional relief..."
whitebox_tools --wd=. -r=DirectionalRelief \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/directional_relief.tif"

# ============================================================================
# 7. TOPOGRAPHIC OPENNESS
# ============================================================================
echo ""
echo "[7/12] Topographic Openness..."

# Positive openness
echo "  - Calculating positive openness..."
whitebox_tools --wd=. -r=MaxAnisotropyDev \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/max_anisotropy_dev.tif"

# Sky-view factor
echo "  - Calculating sky-view factor..."
whitebox_tools --wd=. -r=SkyViewFactor \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/sky_view_factor.tif"

# ============================================================================
# 8. GEOMORPHONS AND LANDFORM CLASSIFICATION
# ============================================================================
echo ""
echo "[8/12] Geomorphons and Landform Classification..."

# Geomorphons
echo "  - Calculating geomorphons..."
whitebox_tools --wd=. -r=Geomorphons \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/geomorphons.tif"

# Pennock landform classification
echo "  - Pennock landform classification..."
whitebox_tools --wd=. -r=PennockLandformClass \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/pennock_landforms.tif"

# ============================================================================
# 9. ASPECT-RELATED ANALYSIS
# ============================================================================
echo ""
echo "[9/12] Aspect-Related Analysis..."

# Aspect (in radians for calculations)
echo "  - Calculating aspect in radians..."
whitebox_tools --wd=. -r=Aspect \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/aspect_radians.tif"

# Eastness
echo "  - Calculating eastness..."
whitebox_tools --wd=. -r=Aspect \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/aspect_temp.tif"

# Northness
echo "  - Calculating northness..."
# Note: These require trigonometric operations on aspect

# ============================================================================
# 10. SCALE-DEPENDENT ANALYSIS
# ============================================================================
echo ""
echo "[10/12] Scale-Dependent Analysis..."

# Gaussian scale space
echo "  - Gaussian scale space analysis..."
for sigma in 1.0 2.0 5.0; do
  echo "    Sigma: $sigma"
  whitebox_tools --wd=. -r=GaussianCurvature \
    --dem="$DEM" \
    -o="$OUTPUT_DIR/gaussian_scale_sigma${sigma}.tif"
done

# ============================================================================
# 11. CONTOURS AND TOPOGRAPHIC FEATURES
# ============================================================================
echo ""
echo "[11/12] Contours and Topographic Features..."

# Contours from raster
echo "  - Generating contour lines (5m interval)..."
whitebox_tools --wd=. -r=ContoursFromRaster \
  --input="$DEM" \
  -o="$OUTPUT_DIR/contours_5m.shp" \
  --interval=5.0

# Contours from raster (10m interval)
echo "  - Generating contour lines (10m interval)..."
whitebox_tools --wd=. -r=ContoursFromRaster \
  --input="$DEM" \
  -o="$OUTPUT_DIR/contours_10m.shp" \
  --interval=10.0

# Find ridges
echo "  - Finding ridges..."
whitebox_tools --wd=. -r=FindRidges \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/ridges.tif"

# ============================================================================
# 12. ILLUMINATION AND VISIBILITY
# ============================================================================
echo ""
echo "[12/12] Illumination and Visibility..."

# Hillshade (multiple sun positions)
echo "  - Creating hillshade variations..."

# Morning sun
whitebox_tools --wd=. -r=Hillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade_morning.tif" \
  --azimuth=90.0 \
  --altitude=30.0

# Midday sun
whitebox_tools --wd=. -r=Hillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade_midday.tif" \
  --azimuth=180.0 \
  --altitude=60.0

# Evening sun
whitebox_tools --wd=. -r=Hillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade_evening.tif" \
  --azimuth=270.0 \
  --altitude=30.0

# Hypsometrically tinted hillshade
echo "  - Creating hypsometrically tinted hillshade..."
whitebox_tools --wd=. -r=HypsometricallyTintedHillshade \
  --dem="$DEM" \
  -o="$OUTPUT_DIR/hillshade_hypsometric.tif"

echo ""
echo "========================================"
echo "GEOMORPHOMETRY WORKFLOW COMPLETED"
echo "Outputs saved to: $OUTPUT_DIR"
echo "========================================"
