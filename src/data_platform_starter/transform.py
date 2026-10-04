import os
from pathlib import Path

from dbt.cli.main import dbtRunner


def dbt_dir() -> Path:
    return Path(os.environ.get("DBT_PROJECT_DIR", "dbt"))


def dbt(*args: str) -> None:
    """Run a dbt command against the project, failing loudly on any error."""
    project = str(dbt_dir())
    result = dbtRunner().invoke(
        [*args, "--project-dir", project, "--profiles-dir", project]
    )
    if not result.success:
        raise SystemExit(f"dbt {' '.join(args)} failed")


def product_schema() -> str:
    """The product schema, including any branch prefix (see generate_schema_name)."""
    prefix = os.environ.get("DBT_SCHEMA_PREFIX", "")
    return f"{prefix}_product" if prefix else "product"
