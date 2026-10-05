# 0002. DuckDB as the default warehouse

**Status:** Accepted
**Date:** 2026-10-04

## Context

A starter platform has to run in seconds on a laptop and in CI, with no accounts, credentials or cost. It also has to show patterns that carry over to the cloud warehouses clients actually run: Snowflake, BigQuery and Databricks.

## Decision

Use DuckDB as the default warehouse, with MotherDuck as the hosted option behind the same dbt adapter. Keep the SQL portable: no DuckDB-only functions in models, so swapping adapters means changing profiles and a few type names, not rewriting logic.

## Consequences

- `invoke demo` and the full test suite run offline in seconds, and CI needs no secrets.
- DuckDB is single-writer, so one process at a time can write to a local file. That's fine for a starter, but a team sharing a warehouse should use MotherDuck or a cloud warehouse.
- Some cloud-only features (for example, Snowflake's zero-copy clones for branch environments) are documented rather than demonstrated.

## Alternatives considered

- **PostgreSQL in Docker:** realistic, but slower, and it needs a running service for every test.
- **Snowflake trial:** closest to production for many clients, but it needs credentials in CI and expires.
