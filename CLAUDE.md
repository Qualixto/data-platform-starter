# CLAUDE.md

Guidance for AI coding agents working in this repository.

## Project

Data Platform Starter: a runnable baseline data platform. dlt loads ECB exchange rates from the Frankfurter API into DuckDB (or MotherDuck), dbt models them through raw → stage → curate → product, and Dagster orchestrates both as one asset graph. Python 3.13, managed with uv.

- `src/data_platform_starter/`: `sources.py` (dlt source), `pipeline.py` (dlt pipeline and destination), `transform.py` (dbt runner), `definitions.py` (Dagster), `fixtures/` (recorded API responses).
- `dbt/`: models in `staging/`, `curated/`, `products/`; data tests in `tests/`; branch-aware schema naming in `macros/`.
- `contracts/`: ODCS contracts for data products.

## Commands

Run everything through uv and invoke from the repository root (dbt paths are relative to it). CI runs the same tasks, so pass them locally before pushing.

```sh
uv run invoke demo       # ingest fixtures, dbt build, print summary (offline)
uv run invoke format     # fix Python and SQL lint and formatting
uv run invoke lint       # ruff, mypy --strict, sqlfluff, version pins
uv run invoke test       # unit, contract and end-to-end tests; fails under 90% coverage
uv run invoke audit      # dependency vulnerability scan
uv run invoke smoke      # build the Docker image and run the demo in it
uv run invoke dagster --fixtures   # Dagster UI with the full asset graph, offline
```

Add dependencies with `uv add <package>` (or `uv add --dev`). Never edit `uv.lock` by hand.

## Data rules

- **Never call the live API in tests or CI.** Use `fetch_fixtures` or a fake `fetch`; record new responses into `fixtures/` when the source changes.
- **Every model and source has `not_empty`.** Give every data test a deliberate severity: `error` when the data is wrong, `warn` when it might be.
- **Product models are contracted.** Changing a product's columns means updating its dbt contract, its ODCS contract in `contracts/`, and bumping the ODCS `version`. `tests/test_contract.py` checks the two match.
- **Loads must stay idempotent.** Rates merge on `(rate_date, base_currency, quote_currency)`; re-running an ingest must not change row counts.
- **Layer discipline.** Staging reads only from sources, curated only from staging, products only from curated.
- SQL is lowercase and linted by sqlfluff with the dbt templater.

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
