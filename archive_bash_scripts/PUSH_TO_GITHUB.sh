#!/bin/bash

# ==============================================================================
# AUTOMATED GITHUB PUSH SCRIPT
# Pushes WhiteboxTools DEM workflows to EOResearchCluster organization
# ==============================================================================

set -e  # Exit on error

REPO_NAME="whitebox-dem-workflows"
ORG_NAME="EOResearchCluster"
REPO_URL="https://github.com/${ORG_NAME}/${REPO_NAME}.git"

echo "============================================"
echo "  GitHub Push Script"
echo "  Repository: ${ORG_NAME}/${REPO_NAME}"
echo "============================================"
echo ""

# Step 1: Initialize git repository
echo "[1/7] Initializing git repository..."
if [ ! -d ".git" ]; then
  git init
  echo "✓ Git repository initialized"
else
  echo "✓ Git repository already exists"
fi

# Step 2: Set main branch
echo ""
echo "[2/7] Setting main branch..."
git branch -M main
echo "✓ Branch set to 'main'"

# Step 3: Add all files
echo ""
echo "[3/7] Adding files to git..."
git add .gitignore
git add LICENSE
git add README.md
git add QUICKSTART.md
git add FIXES.md
git add GITHUB_PUSH_INSTRUCTIONS.md
git add 01_hydrology.sh
git add 02_geomorphometry.sh
git add 03_stream_network.sh
git add 04_morphometry.sh
git add run_all_workflows.sh
git add run_workflows.py
git add view_raster.py
git add utils.sh
echo "✓ All files staged"

# Step 4: Show what will be committed
echo ""
echo "[4/7] Files to be committed:"
git status --short

# Step 5: Create commit
echo ""
echo "[5/7] Creating commit..."
git commit -m "Initial commit: WhiteboxTools DEM analysis workflows

- Add hydrology workflow (depression handling, flow analysis, watersheds)
- Add geomorphometry workflow (slope, curvatures, landforms)
- Add stream network workflow (extraction, ordering, profiles)
- Add morphometry workflow (texture, position, multi-scale analysis)
- Add master shell script (run_all_workflows.sh)
- Add Python wrapper with parallel execution (run_workflows.py)
- Include comprehensive documentation (README, QUICKSTART, FIXES)
- All workflows use only free/open-source WhiteboxTools functions

Features:
- 150+ derived products from a single DEM
- Command-line arguments for all scripts
- Parallel processing support via Python
- Fully documented with examples
- MIT License
"
echo "✓ Commit created"

# Step 6: Add remote
echo ""
echo "[6/7] Adding GitHub remote..."
if git remote | grep -q "origin"; then
  echo "Remote 'origin' already exists. Updating URL..."
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi
echo "✓ Remote added: $REPO_URL"

# Step 7: Push to GitHub
echo ""
echo "[7/7] Pushing to GitHub..."
echo ""
echo "⚠️  You will be prompted for GitHub credentials"
echo "    Username: your-github-username"
echo "    Password: your Personal Access Token"
echo "    (Generate token at: https://github.com/settings/tokens)"
echo ""
read -p "Press Enter to continue..."

if git push -u origin main; then
  echo ""
  echo "============================================"
  echo "  ✓ SUCCESS!"
  echo "============================================"
  echo ""
  echo "Repository URL:"
  echo "  https://github.com/${ORG_NAME}/${REPO_NAME}"
  echo ""
  echo "Next steps:"
  echo "  1. Visit the repository on GitHub"
  echo "  2. Add repository topics/tags"
  echo "  3. Create a release (v1.0.0)"
  echo "  4. Inform your colleagues"
  echo ""
  echo "See GITHUB_PUSH_INSTRUCTIONS.md for details"
  echo ""
else
  echo ""
  echo "============================================"
  echo "  ✗ PUSH FAILED"
  echo "============================================"
  echo ""
  echo "Common issues:"
  echo "  1. Repository doesn't exist on GitHub"
  echo "     → Create it at: https://github.com/organizations/${ORG_NAME}/repositories/new"
  echo ""
  echo "  2. Authentication failed"
  echo "     → Use Personal Access Token as password"
  echo "     → Generate at: https://github.com/settings/tokens"
  echo ""
  echo "  3. No permission"
  echo "     → Request access to ${ORG_NAME} organization"
  echo ""
  echo "See GITHUB_PUSH_INSTRUCTIONS.md for troubleshooting"
  echo ""
  exit 1
fi
