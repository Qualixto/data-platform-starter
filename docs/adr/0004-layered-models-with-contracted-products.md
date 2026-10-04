# 0004. Layered models with contracted data products

**Status:** Accepted
**Date:** 2026-10-04

## Context

Without clear layers, models end up reading from anywhere, consumers depend on intermediate tables, and nobody can change anything safely. Consumers also need a promise about what they can rely on: columns, types, freshness and who to call.

## Decision

Models flow through four layers, each in its own schema: **raw** (as loaded), **stage** (typed and renamed, one model per source table), **curate** (business entities) and **product** (consumer-facing outputs). Each layer reads only from the one before it.

Every product has an enforced dbt model contract and an [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/) contract, kept in step by a test. Data tests carry explicit severities: `error` blocks the build, `warn` alerts.

## Consequences

- Consumers only touch `product`, so everything upstream can be refactored freely.
- Schema drift in a product fails the build instead of reaching consumers.
- The ODCS contract is the publishable artefact for catalogues and data-sharing agreements; dbt enforces it.
- Adding a product is slightly more work: a contract in two places. The test makes forgetting one impossible.

## Alternatives considered

- **Contracts in dbt only:** enforced, but not a standard others can read without dbt.
- **ODCS only:** readable and standard, but nothing stops the SQL drifting from it.
