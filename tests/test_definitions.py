import importlib
from pathlib import Path

import pytest
from dagster import AssetKey


@pytest.mark.usefixtures("dbt_manifest")
def test_dlt_assets_feed_dbt_staging() -> None:
    from data_platform_starter.definitions import defs

    graph = defs.resolve_asset_graph()
    staging = graph.get(AssetKey(["stage", "stg_frankfurter__exchange_rates"]))

    assert staging.parent_keys == {AssetKey(["frankfurter", "exchange_rates"])}


@pytest.mark.usefixtures("dbt_manifest")
def test_full_graph_materialises_offline(
    warehouse: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("USE_FIXTURES", "1")
    from data_platform_starter import definitions

    # The dlt pipeline is built at import, so rebuild it for this warehouse.
    importlib.reload(definitions)

    result = (
        definitions.defs.resolve_implicit_global_asset_job_def().execute_in_process()
    )

    assert result.success
