from datetime import date
from pathlib import Path
from typing import Any

import dlt
import pytest

from data_platform_starter import sources
from data_platform_starter.sources import fetch_fixtures, frankfurter


@pytest.fixture(autouse=True)
def isolated_state(tmp_path: Path) -> None:
    """Iterating a resource directly reads incremental state from the active
    pipeline, so start each test from a fresh one."""
    dlt.pipeline(pipeline_name="source_tests", pipelines_dir=str(tmp_path))


def fake_fetch(path: str, params: dict[str, str]) -> Any:
    if path == "currencies":
        return {"EUR": "Euro", "GBP": "British Pound"}
    return {"rates": {"2026-09-01": {"GBP": 0.85, "USD": 1.1}}}


def test_currencies_yield_code_and_name() -> None:
    rows = list(frankfurter(fetch=fake_fetch).resources["currencies"])

    assert rows == [
        {"code": "EUR", "name": "Euro"},
        {"code": "GBP", "name": "British Pound"},
    ]


def test_exchange_rates_flatten_to_one_row_per_quote() -> None:
    source = frankfurter(start_date=date(2026, 9, 1), fetch=fake_fetch)
    rows = list(source.resources["exchange_rates"])

    assert rows == [
        {
            "rate_date": date(2026, 9, 1),
            "base_currency": "EUR",
            "quote_currency": "GBP",
            "rate": 0.85,
        },
        {
            "rate_date": date(2026, 9, 1),
            "base_currency": "EUR",
            "quote_currency": "USD",
            "rate": 1.1,
        },
    ]


def test_exchange_rates_request_from_start_date() -> None:
    requested: list[tuple[str, dict[str, str]]] = []

    def recording_fetch(path: str, params: dict[str, str]) -> Any:
        requested.append((path, params))
        return {"rates": {}}

    source = frankfurter(
        base="GBP", start_date=date(2026, 9, 15), fetch=recording_fetch
    )
    list(source.resources["exchange_rates"])

    assert requested == [("2026-09-15..", {"base": "GBP"})]


def test_fixtures_filter_rates_from_start() -> None:
    payload = fetch_fixtures("2026-09-29..", {})

    assert sorted(payload["rates"]) == ["2026-09-29", "2026-09-30"]


def test_fetch_api_calls_frankfurter(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, dict[str, str]]] = []

    class Response:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict[str, str]:
            return {"EUR": "Euro"}

    def fake_get(url: str, params: dict[str, str], timeout: int) -> Response:
        calls.append((url, params))
        return Response()

    monkeypatch.setattr("dlt.sources.helpers.requests.get", fake_get)

    assert sources.fetch_api("currencies", {}) == {"EUR": "Euro"}
    assert calls == [("https://api.frankfurter.dev/v1/currencies", {})]
