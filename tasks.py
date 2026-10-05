"""Development tasks. Run with `uv run invoke <task>`; CI runs the same tasks."""

from invoke.context import Context
from invoke.exceptions import Exit
from invoke.tasks import task

IMAGE = "data-platform-starter"


@task
def format(c: Context) -> None:
    """Fix lint issues and format the code."""
    c.run("ruff check --fix", echo=True)
    c.run("ruff format", echo=True)
    c.run("sqlfluff fix dbt/models dbt/tests", echo=True)


@task
def lint(c: Context) -> None:
    """Check version pins, lint, formatting, types and SQL without changing files."""
    c.run("sh scripts/check_python_version.sh", echo=True)
    c.run("ruff check", echo=True)
    c.run("ruff format --check", echo=True)
    c.run("mypy", echo=True)
    c.run("sqlfluff lint dbt/models dbt/tests", echo=True)


@task
def audit(c: Context) -> None:
    """Check locked dependencies for known vulnerabilities."""
    c.run("uv audit --preview-features audit-command", echo=True)


@task
def test(c: Context) -> None:
    """Run the pytest suite with coverage."""
    c.run("pytest", echo=True)


@task
def smoke(c: Context) -> None:
    """Build the Docker image and check it runs the demo end to end."""
    c.run(f"docker build -t {IMAGE} .", echo=True)
    result = c.run(f"docker run --rm {IMAGE} demo", echo=True)
    if result is None or "fx_rates_gbp: 660 rows" not in result.stdout:
        raise Exit("Container did not build the FX product")


@task
def demo(c: Context) -> None:
    """Ingest the offline fixtures, build every model and print a summary."""
    c.run("data-platform-starter demo", echo=True, pty=True)


@task
def ingest(c: Context, fixtures: bool = False, start_date: str = "") -> None:
    """Load exchange rates with dlt, from the live API unless --fixtures."""
    args = (" --fixtures" if fixtures else "") + (
        f" --start-date {start_date}" if start_date else ""
    )
    c.run(f"data-platform-starter ingest{args}", echo=True, pty=True)


@task
def build(c: Context) -> None:
    """Build and test all dbt models."""
    c.run("data-platform-starter build", echo=True, pty=True)


@task
def freshness(c: Context) -> None:
    """Check source freshness against the live data."""
    c.run("dbt source freshness --project-dir dbt --profiles-dir dbt", echo=True)


@task
def dagster(c: Context, fixtures: bool = False) -> None:
    """Open the Dagster UI on :3000 with the full asset graph."""
    env = {"USE_FIXTURES": "1"} if fixtures else {}
    c.run("dagster dev -m data_platform_starter.definitions", env=env, pty=True)
