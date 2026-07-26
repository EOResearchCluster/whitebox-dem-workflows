# Repository Guidelines

## Project Structure & Module Organization

The numbered Bash workflows are the primary entry points: `01_hydrology.sh`,
`02_geomorphometry.sh`, `03_stream_network.sh`, and `04_morphometry.sh`.
`run_all_workflows.sh` orchestrates the full sequence, while
`run_workflows.py` provides the Python CLI. Shared helpers include
`view_raster.py`, `tiffplot.py`, and `utils.sh`. Keep user-facing documentation
at the repository root; implementation plans and specifications belong under
`docs/superpowers/`. Treat `outputs/`, `logs/`, `.pixi/`, and local DEM files
as generated or machine-local material.

## Build, Test, and Development Commands

Run `pixi install` to create the project environment. Use `pixi run run-all`
to process the root `dem.tif`, or provide an input explicitly with
`./run_all_workflows.sh path/to/dem.tif`. Run one stage with, for example,
`./01_hydrology.sh path/to/dem.tif`; substitute the appropriate numbered
workflow as needed. `python run_workflows.py --list` is a no-processing CLI
smoke check.

## Coding Style & Naming Conventions

Use two-space indentation in Bash, quote paths, and name configuration
variables in uppercase, such as `DEM` and `OUTPUT_DIR`. Reusable shell and
Python functions use `snake_case`. Python uses four spaces, `pathlib.Path`,
useful type hints, and standard-library imports before third-party imports.
Preserve the numbered workflow filenames.

## Testing Guidelines

This repository has no automated test suite, coverage target, formatter, or
CI pipeline. Run `bash -n *.sh` and relevant Python help or list smoke
commands. For workflow changes, use a small representative DEM and a
disposable output directory, for example
`./01_hydrology.sh test-dem.tif /tmp/whitebox-hydrology`. Workflow signatures
differ, so use each script header as authority. Inspect output rasters and
logs: current runners may report success after an inner WhiteboxTools failure.
Add focused regression tests under `tests/` when practical.

## Commit & Pull Request Guidelines

Recent history uses short imperative subjects, for example `enable logging`
and `pixi bump`. Keep commits focused by workflow. PRs should state DEM
characteristics, exact commands, observed outputs, and known failures; link
issues and include screenshots only for visualization changes.

## Data & Configuration Hygiene

Do not commit DEMs, generated rasters, `outputs/`, `logs/`, `.pixi/`, secrets,
or machine-specific paths. Update `pixi.toml` whenever dependencies or tasks
change.
