import os
from datetime import date
from pathlib import Path

import dlt
from dlt.common.pipeline import LoadInfo
from dlt.sources import DltSource

from data_platform_starter.sources import fetch_api, fetch_fixtures, frankfurter

RAW_DATASET = "raw_frankfurter"
FIXTURES_START = date(2026, 9, 1)


def warehouse_path() -> Path:
    return Path(os.environ.get("WAREHOUSE_PATH", "data/warehouse.duckdb"))


def make_pipeline() -> dlt.Pipeline:
    """Load into local DuckDB, or MotherDuck when ``DESTINATION=motherduck``.

    MotherDuck credentials come from dlt's usual config, e.g. the
    ``DESTINATION__MOTHERDUCK__CREDENTIALS`` environment variable.
    """
    path = warehouse_path()
    destination: dlt.destinations.duckdb | dlt.destinations.motherduck
    if os.environ.get("DESTINATION") == "motherduck":
        destination = dlt.destinations.motherduck()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        destination = dlt.destinations.duckdb(str(path))
    return dlt.pipeline(
        pipeline_name="frankfurter",
        destination=destination,
        dataset_name=RAW_DATASET,
        # Keep pipeline state next to the warehouse it describes, so a fresh
        # warehouse never inherits incremental state from another one.
        pipelines_dir=str(path.parent / ".dlt"),
    )


def make_source(
    *, fixtures: bool | None = None, start_date: date | None = None
) -> DltSource:
    """The Frankfurter source, reading recorded fixtures when asked or when
    ``USE_FIXTURES`` is set, so Dagster and the demo can run offline."""
    if fixtures is None:
        fixtures = bool(os.environ.get("USE_FIXTURES"))
    if fixtures:
        return frankfurter(
            start_date=start_date or FIXTURES_START, fetch=fetch_fixtures
        )
    return frankfurter(start_date=start_date, fetch=fetch_api)


def ingest(*, fixtures: bool | None = None, start_date: date | None = None) -> LoadInfo:
    return make_pipeline().run(make_source(fixtures=fixtures, start_date=start_date))
