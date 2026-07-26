# Repository Contributor Documentation Design

## Goal

Create a concise `AGENTS.md` contributor guide and make the existing README
more practical and accurate. Documentation must reflect the current checkout,
including its lack of automated tests and its known execution-status problems.

## AGENTS.md

The guide will be approximately 250–350 words and use the required
`Repository Guidelines` title. It will cover:

- the four numbered Bash workflows, orchestration scripts, Python utilities,
  root-level documentation, and ignored generated data;
- Pixi installation and workflow commands;
- existing Bash and Python style, including indentation, variable naming,
  quoting, type hints, and file naming;
- the current manual validation baseline: Bash syntax checks, Python CLI smoke
  checks, and a representative small-DEM run with output inspection;
- short imperative commit messages and evidence expected in pull requests;
- avoiding committed DEMs, generated outputs, logs, secrets, and local
  environments.

It will not claim that a test framework, formatter, coverage target, or CI
pipeline exists.

## README.md

Apply focused corrections rather than a wholesale rewrite:

- replace unsupported marketing language such as “Production Ready” and
  “150+ derived products” with factual descriptions;
- retain the quick-start commands and workflow overview;
- state that Pixi tasks use `dem.tif` by default and show how to pass another
  DEM through direct scripts or the Python wrapper;
- add a brief current-limitations note covering absent automated tests,
  unreliable success propagation, Python stream-network argument handling,
  the broken `compare_rasters` helper, and tool-version compatibility;
- keep detailed installation material linked instead of duplicating it.

## Boundaries and Verification

Do not change workflow code, generated files, or the user’s existing
uncommitted script changes. Verify Markdown structure and links, check that
`AGENTS.md` remains within 200–400 words, rerun shell/Python syntax checks, and
review the final diff for concise, repository-specific language.
