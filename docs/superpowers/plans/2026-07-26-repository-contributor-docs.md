# Repository Contributor Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a concise repository-specific contributor guide and correct misleading README guidance without changing workflow code.

**Architecture:** `AGENTS.md` will be the short contributor contract; `README.md` will remain the operator-facing entry point. Both documents will describe the current repository honestly, including manual verification and known limitations.

**Tech Stack:** Markdown, Bash, Python 3, Pixi, WhiteboxTools

---

### Task 1: Add the contributor guide

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Reconfirm the overwrite guard**

Run:

```bash
test ! -e AGENTS.md
```

Expected: exit status `0`. If it fails, stop without modifying `AGENTS.md`.

- [ ] **Step 2: Create the repository-specific guide**

Create `AGENTS.md` with the title `Repository Guidelines` and these sections:

```markdown
# Repository Guidelines

## Project Structure & Module Organization

The numbered Bash scripts are the core workflows: `01_hydrology.sh`,
`02_geomorphometry.sh`, `03_stream_network.sh`, and `04_morphometry.sh`.
`run_all_workflows.sh` orchestrates them; `run_workflows.py` provides a Python
CLI. Raster helpers live in `view_raster.py`, `tiffplot.py`, and `utils.sh`.
Installation and usage notes are root-level Markdown files. Treat `outputs/`,
`logs/`, `.pixi/`, and local DEM files as generated or machine-local assets.

## Build, Test, and Development Commands

Run `pixi install` to create the project environment. `pixi run run-all` uses
`dem.tif`; for another input, use `./run_all_workflows.sh path/to/dem.tif`.
Run one stage with `./01_hydrology.sh path/to/dem.tif`, substituting the
appropriate numbered script. `python run_workflows.py --list` checks the Python
CLI without processing a DEM.

## Coding Style & Naming Conventions

Use two-space indentation in Bash, quote path variables, and keep configuration
variables uppercase (`DEM`, `OUTPUT_DIR`). Name reusable shell functions and
Python functions in `snake_case`. Python uses four spaces, `pathlib.Path`, type
hints where useful, and standard-library imports before third-party imports.
Keep workflow filenames numbered so execution order remains obvious.

## Testing Guidelines

There is currently no automated test suite, coverage target, formatter, or CI
pipeline. Before submitting changes, run `bash -n *.sh` and exercise relevant
Python help or list commands. Test workflow changes with a small representative
DEM and a disposable output directory. Inspect expected rasters and logs;
current runners can report success after an inner WhiteboxTools failure.
Regression fixes should add a focused test under `tests/` when practical.

## Commit & Pull Request Guidelines

Recent history uses short imperative subjects such as `enable logging` and
`pixi bump`. Keep commits focused and describe the affected workflow. Pull
requests should state the input DEM characteristics, exact commands run,
observed outputs, and known failures. Link issues and include screenshots only
for visualization changes.

## Data & Configuration Hygiene

Do not commit DEMs, generated rasters, `outputs/`, `logs/`, `.pixi/`, secrets,
or machine-specific paths. Update `pixi.toml` when dependencies or tasks change.
```

- [ ] **Step 3: Verify structure and length**

Run:

```bash
head -1 AGENTS.md
wc -w AGENTS.md
rg '^## ' AGENTS.md
```

Expected: title is `# Repository Guidelines`, word count is 200–400, and all
six section headings are present.

- [ ] **Step 4: Commit the guide**

```bash
git add AGENTS.md
git commit -m "docs: add repository contributor guide"
```

### Task 2: Make the README factual and practical

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace marketing claims with a scope summary**

Replace the `## Features` list with a `## Scope` section that states the
repository contains four DEM workflows, a Bash/Python orchestration layer,
over 100 requested primary outputs whose availability varies by WhiteboxTools
version, and raster inspection helpers. State that this is a research workflow
collection rather than a fully verified production pipeline.

Use:

```markdown
## Scope

This repository provides:

- four numbered workflows for hydrology, geomorphometry, stream networks, and
  morphometry;
- Bash and Python entry points for sequential execution;
- more than 100 requested primary outputs, depending on conditional steps and
  the installed WhiteboxTools build;
- lightweight raster inspection and plotting helpers.

This is a research workflow collection, not a fully verified production
pipeline. Review the limitations below before starting a long run.
```

- [ ] **Step 2: Clarify command defaults**

After the Pixi task examples, add:

```markdown
Pixi workflow tasks use `dem.tif` in the repository root. To select another
input path, call the Bash or Python entry points below.
```

Keep the existing direct-script and Python examples.

- [ ] **Step 3: Add current limitations**

Add a concise `## Current Limitations` section after the Python wrapper:

```markdown
- No automated tests or CI are configured.
- Bash and Pixi runners may mask an inner WhiteboxTools failure; verify logs
  and expected output files instead of trusting the completion banner.
- The Python wrapper currently passes incorrect positional arguments to the
  stream-network workflow. Run `03_stream_network.sh` directly after hydrology.
- `compare_rasters` in `utils.sh` currently fails to forward its arguments.
- Tool availability depends on the WhiteboxTools build. Version 2.4.0 does not
  provide every command referenced by these scripts, so check long workflows
  with `whitebox_tools --toolhelp=ToolName`.
```

Remove the broken `compare_rasters` example from the utility command block.

- [ ] **Step 4: Correct the output description and footer**

Replace per-directory file-count promises with descriptions of each output
directory. State that output totals vary with conditional steps, tool version,
and failures. Remove the decorative “Made with” footer.

Use:

```markdown
## Output Structure

| Directory | Contents |
|---|---|
| `outputs/01_hydrology/` | Flow routing, accumulation, basins, and indices |
| `outputs/02_geomorphometry/` | Terrain attributes, curvature, and landforms |
| `outputs/03_stream_network/` | Extracted streams, ordering, and profiles |
| `outputs/04_morphometry/` | Multi-scale terrain and topology metrics |

Output totals vary with conditional steps, the installed WhiteboxTools build,
and failed tools. Treat expected files—not directory counts—as completion
criteria.
```

- [ ] **Step 5: Review the README diff**

Run:

```bash
git diff -- README.md
rg -n 'Production Ready|150\\+|~150|compare_rasters dem' README.md
```

Expected: the diff is limited to the sections above and the search returns no
matches.

- [ ] **Step 6: Commit the README correction**

```bash
git add README.md
git commit -m "docs: clarify workflow status and usage"
```

### Task 3: Verify the documentation change

**Files:**
- Verify: `AGENTS.md`
- Verify: `README.md`

- [ ] **Step 1: Run non-destructive syntax checks**

```bash
bash -n 01_hydrology.sh 02_geomorphometry.sh 03_stream_network.sh \
  04_morphometry.sh run_all_workflows.sh utils.sh
python -m compileall -q run_workflows.py view_raster.py tiffplot.py
```

Expected: exit status `0` for both commands.

- [ ] **Step 2: Run CLI smoke checks**

```bash
python run_workflows.py --help
python tiffplot.py --help
MPLCONFIGDIR=/tmp python view_raster.py --help
```

Expected: each command exits `0` and prints usage text.

- [ ] **Step 3: Check whitespace and scope**

```bash
git diff --check HEAD~2..HEAD
git status --short
```

Expected: no whitespace errors; only the user’s pre-existing workflow-script
status remains outside the two documentation commits.
