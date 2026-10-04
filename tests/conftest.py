from collections.abc import Iterator
from pathlib import Path

import pytest

from data_platform_starter.transform import dbt


@pytest.fixture
def warehouse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Point the pipeline and dbt at a fresh, empty warehouse."""
    path = tmp_path / "warehouse.duckdb"
    monkeypatch.setenv("WAREHOUSE_PATH", str(path))
    monkeypatch.delenv("DBT_SCHEMA_PREFIX", raising=False)
    yield path


@pytest.fixture(scope="session")
def dbt_manifest() -> None:
    """Dagster reads the dbt manifest at import, so parse the project first."""
    dbt("parse", "--quiet")
