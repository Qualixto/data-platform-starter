# Data Platform Starter

A runnable baseline data platform: dlt, DuckDB/MotherDuck, dbt and Dagster, with data contracts, quality gates and CI

## Getting started

Requires [uv](https://docs.astral.sh/uv/) and Docker.

```sh
uv sync
uv run pre-commit install
uv run data-platform-starter Ada
```

## Development

Every check runs through [invoke](https://www.pyinvoke.org), and CI runs the same tasks, so a green local run means a green pipeline.

| Task | What it does |
|---|---|
| `uv run invoke format` | Fix lint issues and format the code |
| `uv run invoke lint` | Version pins, ruff, formatting and mypy (strict) |
| `uv run invoke test` | pytest with branch coverage (fails under 90%) |
| `uv run invoke audit` | Check locked dependencies for known vulnerabilities |
| `uv run invoke smoke` | Build the Docker image and check it starts |

pre-commit runs ruff, mypy, secrets scanning (gitleaks) and commit message checks on every commit, and the test suite before every push.

## Conventions

- Start from an issue, and branch as `<type>/<issue>-<short-description>`.
- Commit as `<type>: <description>` using `feat`, `fix`, `refactor`, `test`, `docs`, `chore` or `perf`.
- Work is done when it meets the [Definition of Done](DEFINITION_OF_DONE.md).
- Record significant decisions in [`docs/adr/`](docs/adr/).

## Project layout

```
src/data_platform_starter/     application code
tests/                  pytest suite
docs/adr/               architecture decision records
tasks.py                development tasks, shared with CI
```

## Updating from the template

This project was generated from [Qualixto/python-template](https://github.com/Qualixto/python-template). Pull in later template improvements with:

```sh
uvx copier update --trust
```
