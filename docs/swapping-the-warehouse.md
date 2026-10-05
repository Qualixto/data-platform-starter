# Swapping the warehouse

The models avoid DuckDB-specific SQL, so moving to a cloud warehouse is mostly configuration. These are the changes.

---

## 1. Install the adapters

| Warehouse | dlt extra | dbt adapter |
|---|---|---|
| Snowflake | `dlt[snowflake]` | `dbt-snowflake` |
| BigQuery | `dlt[bigquery]` | `dbt-bigquery` |
| Databricks | `dlt[databricks]` | `dbt-databricks` |

```sh
uv add "dlt[snowflake]" dbt-snowflake
```

## 2. Point dlt at it

In `pipeline.py`, add a branch to `make_pipeline`, for example:

```python
elif os.environ.get("DESTINATION") == "snowflake":
    destination = dlt.destinations.snowflake()
```

Credentials come from dlt's standard config, such as `DESTINATION__SNOWFLAKE__CREDENTIALS`, or `.dlt/secrets.toml` locally (keep it out of git).

## 3. Add a dbt target

Add an output to `dbt/profiles.yml` that reads its credentials from environment variables, and select it with `DBT_TARGET`:

```yaml
    snowflake:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      authenticator: snowflake_jwt
      private_key_path: "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PATH') }}"
      role: transformer
      warehouse: transforming
      database: analytics
      schema: main
      threads: 8
```

## 4. Adjust contract types

Enforced contracts compare exact types. Update `data_type` in `_products__models.yml` and `physicalType` in the ODCS contract, for example `double` → `float` on Snowflake, or `float64` and `string` on BigQuery. `tests/test_contract.py` keeps the two aligned.

## 5. Use the warehouse's strengths in CI

- **Branch builds:** `DBT_SCHEMA_PREFIX` works unchanged. On Snowflake, consider zero-copy cloning production into the prefixed schemas, so pull requests test against real data.
- **Slim CI:** with a shared production warehouse, store the production `manifest.json` and run `dbt build --select state:modified+ --defer --state <path>`, so CI only rebuilds what changed.
- **Freshness:** run `invoke freshness` on a schedule against production, and alert on warnings.
