# Default must match .python-version: scripts/check_python_version.sh enforces it.
ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Dependencies first, so code changes don't invalidate the cached layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --locked --no-dev --no-editable

RUN useradd --system --no-create-home app
USER app

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["data-platform-starter"]
