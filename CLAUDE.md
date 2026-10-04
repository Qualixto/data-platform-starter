# CLAUDE.md

Guidance for AI coding agents working in this repository.

## Project

Data Platform Starter: A runnable baseline data platform: dlt, DuckDB/MotherDuck, dbt and Dagster, with data contracts, quality gates and CI. Python 3.13, managed with uv, source in `src/data_platform_starter/`.

## Commands

Run everything through uv and invoke. CI runs the same tasks, so pass them locally before pushing.

```sh
uv run invoke format     # fix lint and formatting
uv run invoke lint       # ruff, format check, mypy --strict, version pins
uv run invoke test       # pytest with coverage (fails under 90%)
uv run invoke audit      # dependency vulnerability scan
uv run invoke smoke      # build and start the Docker image
```

Add dependencies with `uv add <package>` (or `uv add --dev`). Never edit `uv.lock` by hand.

## Conventions

- **Issues first.** Branch as `<type>/<issue>-<short-description>`, for example `feat/12-add-retries`.
- **Commits** are `<type>: <description>` with types `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf` only. CI and tooling changes are `chore`. A commit-msg hook enforces this.
- **No AI attribution.** Never add `Co-Authored-By` trailers or "Generated with" footers to commits, pull requests, issues or comments.
- **Comments explain why, not what.** Only add one when the reason isn't visible in the code.
- **Type hints everywhere.** mypy runs in strict mode over `src`, `tests` and `tasks.py`.
- **Test new behaviour.** Cover failure paths, not just the happy path.
- Python version lives in `.python-version`; the Dockerfile default must match it, and `invoke lint` checks this.
- Record significant decisions as ADRs in `docs/adr/`, and check work against `DEFINITION_OF_DONE.md`.
- `.copier-answers.yml` is managed by Copier. Don't edit it; use `uvx copier update --trust`.
