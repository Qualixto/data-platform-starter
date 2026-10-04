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


@task
def lint(c: Context) -> None:
    """Check version pins, lint, formatting, and types without changing files."""
    c.run("sh scripts/check_python_version.sh", echo=True)
    c.run("ruff check", echo=True)
    c.run("ruff format --check", echo=True)
    c.run("mypy", echo=True)


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
    """Build the Docker image and check the container runs."""
    c.run(f"docker build -t {IMAGE} .", echo=True)
    result = c.run(f"docker run --rm {IMAGE} smoke", echo=True)
    if result is None or "Hello, smoke!" not in result.stdout:
        raise Exit("Container did not print the expected greeting")
