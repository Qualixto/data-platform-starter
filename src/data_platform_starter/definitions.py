"""Dagster code location: dlt ingestion and dbt models as one asset graph.

Run locally with ``uv run invoke dagster``.
"""

from collections.abc import Iterator
from typing import Any

from dagster import (
    AssetExecutionContext,
    AssetKey,
    AssetSelection,
    AssetSpec,
    Definitions,
    ScheduleDefinition,
)
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dlt.translator import DltResourceTranslatorData

from data_platform_starter.pipeline import make_pipeline, make_source
from data_platform_starter.transform import dbt_dir

dbt_project = DbtProject(
    project_dir=dbt_dir().resolve(), profiles_dir=dbt_dir().resolve()
)
dbt_project.prepare_if_dev()


class RawLayerTranslator(DagsterDltTranslator):
    """Key dlt assets as dbt sees them (``frankfurter/<table>``), so the two connect."""

    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        return (
            super()
            .get_asset_spec(data)
            .replace_attributes(
                key=AssetKey(["frankfurter", data.resource.name]), deps=[]
            )
        )


@dlt_assets(
    dlt_source=make_source(),
    dlt_pipeline=make_pipeline(),
    name="frankfurter",
    group_name="raw",
    dagster_dlt_translator=RawLayerTranslator(),
)
def frankfurter_assets(
    context: AssetExecutionContext, dlt: DagsterDltResource
) -> Iterator[Any]:
    yield from dlt.run(context=context)


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource) -> Iterator[Any]:
    yield from dbt.cli(["build"], context=context).stream()


# The ECB publishes at around 16:00 CET on business days.
daily_refresh = ScheduleDefinition(
    name="daily_refresh",
    target=AssetSelection.all(),
    cron_schedule="0 17 * * 1-5",
    execution_timezone="Europe/London",
)

defs = Definitions(
    assets=[frankfurter_assets, dbt_models],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
    schedules=[daily_refresh],
)
