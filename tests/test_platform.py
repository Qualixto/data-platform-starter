"""End-to-end: ingest fixtures with dlt, build and test every dbt model."""

from pathlib import Path

import duckdb
import pytest

from data_platform_starter.__main__ import main
from data_platform_starter.pipeline import ingest
from data_platform_starter.transform import dbt


def count(warehouse: Path, table: str) -> int:
    with duckdb.connect(str(warehouse)) as con:
        result = con.execute(f"select count(*) from {table}").fetchone()  # noqa: S608
    assert result is not None
    return int(result[0])


def test_demo_builds_the_product(
    warehouse: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["demo"])

    assert "fx_rates_gbp: 660 rows, latest 2026-09-30" in capsys.readouterr().out


def test_reingest_is_idempotent(warehouse: Path) -> None:
    ingest(fixtures=True)
    first = count(warehouse, "raw_frankfurter.exchange_rates")

    ingest(fixtures=True)

    assert count(warehouse, "raw_frankfurter.exchange_rates") == first == 638


def test_schema_prefix_isolates_a_build(
    warehouse: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DBT_SCHEMA_PREFIX", "pr_42")
    ingest(fixtures=True)
    dbt("build", "--select", "+fx_rates_gbp")

    assert count(warehouse, "pr_42_product.fx_rates_gbp") == 660


def test_cli_ingest_and_build(
    warehouse: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["ingest", "--fixtures"])
    main(["build"])

    assert "raw_frankfurter" in capsys.readouterr().out
    assert count(warehouse, "product.fx_rates_gbp") == 660


def test_failed_dbt_command_exits(warehouse: Path) -> None:
    with pytest.raises(SystemExit, match="dbt build --select fx_rates_gbp failed"):
        dbt("build", "--select", "fx_rates_gbp")
