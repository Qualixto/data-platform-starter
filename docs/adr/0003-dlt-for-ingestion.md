# 0003. dlt for ingestion

**Status:** Accepted
**Date:** 2026-10-04

## Context

Ingestion code tends to grow its own retry logic, schema handling, state tracking and loaders, one source at a time. That's where connector delivery slows from weeks to months.

## Decision

Write sources with dlt. Each source is a plain Python generator; dlt handles schema inference and evolution, incremental state, merge semantics and loading to any supported destination.

Sources take their HTTP access as a `fetch` argument, so tests and CI swap in recorded fixtures without mocking libraries.

## Consequences

- A new REST source is typically a few dozen lines, plus fixtures and tests.
- Incremental state lives in the destination as well as locally, so a fresh environment resumes correctly.
- dlt and Dagster integrate through `dagster-dlt`, so each resource shows up as an asset with lineage into dbt.

## Alternatives considered

- **Hand-written loaders:** full control, but every source re-implements state, retries and schema handling.
- **Managed connectors (Fivetran, Airbyte):** fast for common SaaS sources, but they add cost and a separate platform, and they don't cover bespoke APIs well.
