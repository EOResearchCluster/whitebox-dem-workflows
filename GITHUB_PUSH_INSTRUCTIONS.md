# Instructions for Pushing to GitHub

## Repository Setup

### Suggested Repository Name
```
whitebox-dem-workflows
```

**Alternative names:**
- `whitebox-terrain-analysis`
- `dem-geoprocessing-toolkit`
- `whitebox-hydro-geomorph`

### Repository Description
```
Comprehensive DEM analysis workflows for WhiteboxTools: hydrology, geomorphometry, stream networks, and morphometry using free/open-source tools
```

### Topics/Tags (for GitHub)
```
whitebox-tools, dem-analysis, hydrology, geomorphometry, terrain-analysis,
geoprocessing, geospatial, watershed-analysis, python, bash, open-source
```

---

## Step-by-Step Instructions

### 1. Prepare the Repository Locally

```bash
# Navigate to the project directory
cd /Volumes/maysys/hydrostuff/whitebox/dettelbach

# Initialize git repository (if not already done)
git init

# Rename main branch to 'main' (GitHub standard)
git branch -M main
```

### 2. Create .gitignore File

```bash
cat > .gitignore << 'EOF'
# DEM Files (don't commit large rasters)
*.tif
*.tiff
*.img
*.bil

# Output directories
outputs/
logs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# OS
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# IDE
.vscode/
.idea/
*.sublime-*

# Temporary files
*.tmp
*.bak
*.log
EOF
```

### 3. Organize Files for GitHub

```bash
# Move GITHUB_README.md to README.md (GitHub standard)
mv GITHUB_README.md README.md

# Keep QUICKSTART.md and FIXES.md as-is

# Optional: Create a .github directory for GitHub-specific files
mkdir -p .github
```

### 4. Create GitHub Repository

**Option A: Via GitHub Web Interface (Recommended)**

1. Go to: https://github.com/organizations/EOResearchCluster/repositories/new
2. Fill in:
   - **Repository name**: `whitebox-dem-workflows`
   - **Description**: `Comprehensive DEM analysis workflows for WhiteboxTools: hydrology, geomorphometry, stream networks, and morphometry using free/open-source tools`
   - **Visibility**: Public (or Private if needed)
   - **DO NOT** initialize with README, .gitignore, or license (we have these locally)
3. Click "Create repository"

**Option B: Via GitHub CLI (if installed)**

```bash
# Install gh CLI if needed
brew install gh

# Authenticate
gh auth login

# Create repository in your organization
gh repo create EOResearchCluster/whitebox-dem-workflows \
  --public \
  --description "Comprehensive DEM analysis workflows for WhiteboxTools" \
  --source=. \
  --remote=origin
```

### 5. Add and Commit Files

```bash
# Add all workflow files
git add 01_hydrology.sh
git add 02_geomorphometry.sh
git add 03_stream_network.sh
git add 04_morphometry.sh
git add run_all_workflows.sh
git add run_workflows.py

# Add documentation
git add README.md
git add QUICKSTART.md
git add FIXES.md
git add LICENSE

# Add .gitignore
git add .gitignore

# Create initial commit
git commit -m "Initial commit: WhiteboxTools DEM analysis workflows

- Add hydrology workflow (depression handling, flow analysis, watersheds)
- Add geomorphometry workflow (slope, curvatures, landforms)
- Add stream network workflow (extraction, ordering, profiles)
- Add morphometry workflow (texture, position, multi-scale analysis)
- Add master shell script (run_all_workflows.sh)
- Add Python wrapper with parallel execution (run_workflows.py)
- Include comprehensive documentation (README, QUICKSTART, FIXES)
- All workflows use only free/open-source WhiteboxTools functions
"
```

### 6. Connect to GitHub and Push

```bash
# Add remote (replace with your actual GitHub URL)
git remote add origin https://github.com/EOResearchCluster/whitebox-dem-workflows.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

### 7. Verify on GitHub

1. Go to: https://github.com/EOResearchCluster/whitebox-dem-workflows
2. Verify all files are present
3. Check that README.md displays correctly
4. Verify LICENSE is recognized by GitHub

---

## Post-Push Configuration

### 8. Add Repository Topics

1. Go to repository page
2. Click gear icon next to "About"
3. Add topics:
   - `whitebox-tools`
   - `dem-analysis`
   - `hydrology`
   - `geomorphometry`
   - `terrain-analysis`
   - `geoprocessing`
   - `geospatial`
   - `watershed-analysis`
   - `python`
   - `bash`
   - `open-source`

### 9. Create Release (Optional but Recommended)

```bash
# Tag the current version
git tag -a v1.0.0 -m "Initial release: Complete DEM analysis workflows"

# Push tag to GitHub
git push origin v1.0.0
```

Or via GitHub web interface:
1. Go to "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description:
```
## WhiteboxTools DEM Analysis Workflows v1.0.0

First stable release of comprehensive DEM analysis workflows.

### Features
- ✅ Complete hydrology workflow (30+ outputs)
- ✅ Complete geomorphometry workflow (50+ outputs)
- ✅ Complete stream network workflow (25+ outputs)
- ✅ Complete morphometry workflow (30+ outputs)
- ✅ Python wrapper with parallel execution
- ✅ Command-line argument support for all scripts
- ✅ Only free/open-source WhiteboxTools functions
- ✅ Comprehensive documentation

### Requirements
- WhiteboxTools (free version)
- Bash (macOS/Linux)
- Python 3.6+ (optional, for parallel execution)

### Quick Start
\`\`\`bash
./run_all_workflows.sh your_dem.tif
\`\`\`

See README.md for complete documentation.
```

### 10. Enable GitHub Pages (Optional - for documentation)

1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs` or `/ (root)`
4. Save

This will make documentation accessible at:
`https://eoresearchcluster.github.io/whitebox-dem-workflows/`

### 11. Add Collaborators

1. Go to Settings → Collaborators
2. Add team members with appropriate permissions:
   - **Admin**: Full access
   - **Write**: Can push commits
   - **Read**: Can view and clone

---

## Maintenance Workflow

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/add-new-analysis

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add new terrain analysis tool"

# Push to GitHub
git push origin feature/add-new-analysis

# Create Pull Request on GitHub
```

### Updating Main Branch

```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Merge feature branch (if working locally)
git merge feature/add-new-analysis

# Push to GitHub
git push origin main
```

---

## Informing Colleagues

### Email Template

**Subject:** New GitHub Repository: WhiteboxTools DEM Analysis Workflows

Hi team,

I've created a new repository with comprehensive DEM analysis workflows using WhiteboxTools:

🔗 **Repository:** https://github.com/EOResearchCluster/whitebox-dem-workflows

### What it does:
- Automated hydrology analysis (flow routing, watersheds, wetness indices)
- Complete geomorphometry (slope, curvatures, landforms)
- Stream network extraction and analysis
- Advanced morphometric analysis
- 150+ derived products from a single DEM

### Key features:
✅ Only uses FREE WhiteboxTools functions (no license needed)
✅ Shell scripts with CLI arguments
✅ Python wrapper with parallel execution support
✅ Fully documented with examples

### Quick Start:
```bash
# Clone repository
git clone https://github.com/EOResearchCluster/whitebox-dem-workflows.git
cd whitebox-dem-workflows

# Install WhiteboxTools
pixi global install whitebox_tools

# Run analysis
./run_all_workflows.sh your_dem.tif
```

Check README.md and QUICKSTART.md for complete documentation.

Questions? Open an issue on GitHub or contact me directly.

Best regards,
[Your Name]

---

### Slack/Teams Announcement

```
📢 New Repository Alert!

🗺️ **WhiteboxTools DEM Analysis Workflows**
https://github.com/EOResearchCluster/whitebox-dem-workflows

Comprehensive DEM processing workflows for:
• Hydrology (flow, watersheds, TWI)
• Geomorphometry (slope, curvatures, landforms)
• Stream networks (extraction, ordering, profiles)
• Morphometry (texture, position, multi-scale)

🎯 150+ outputs from a single DEM
✅ 100% free tools (no license needed)
🚀 Parallel processing support
📚 Fully documented

Clone it, star it, use it! 🎉
```

---

## Troubleshooting

### Authentication Issues

```bash
# Use GitHub Personal Access Token
# Generate at: https://github.com/settings/tokens

# Use token as password when prompted
git push origin main
Username: your-github-username
Password: [paste token here]

# Or configure credential helper
git config --global credential.helper store
```

### Permission Denied

```bash
# Check if you have access to the organization
gh auth status

# Request access from organization admin if needed
```

### Large File Warnings

```bash
# If you accidentally committed large DEM files
git rm --cached *.tif
git commit -m "Remove large DEM files"
git push origin main
```

---

## Next Steps

After pushing to GitHub:

1. ✅ Verify repository is accessible to team
2. ✅ Add meaningful repository description
3. ✅ Create initial release (v1.0.0)
4. ✅ Inform colleagues via email/Slack
5. ✅ Add to team documentation/wiki
6. ✅ Create GitHub wiki pages (optional)
7. ✅ Set up GitHub Actions for CI/CD (optional)
8. ✅ Add example DEM or test data (optional)

---

## Support

If you need help:
- GitHub Issues: https://github.com/EOResearchCluster/whitebox-dem-workflows/issues
- Organization Admins: [list admin contacts]
- Documentation: README.md in repository

---

**Ready to push? Run the commands in Section 5-6 above!**
