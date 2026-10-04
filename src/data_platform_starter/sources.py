"""dlt source for ECB reference exchange rates, published by the Frankfurter API."""

import json
from collections.abc import Callable, Iterator
from datetime import date, timedelta
from importlib.resources import files
from typing import Any

import dlt
from dlt.sources import DltResource, incremental
from dlt.sources.helpers import requests

BASE_URL = "https://api.frankfurter.dev/v1"

Fetch = Callable[[str, dict[str, str]], Any]


def fetch_api(path: str, params: dict[str, str]) -> Any:
    response = requests.get(f"{BASE_URL}/{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_fixtures(path: str, params: dict[str, str]) -> Any:
    """Serve recorded API responses, so the platform runs offline and in CI."""
    fixtures = files("data_platform_starter.fixtures")
    if path == "currencies":
        return json.loads(fixtures.joinpath("currencies.json").read_text())
    payload = json.loads(fixtures.joinpath("rates.json").read_text())
    start = path.removesuffix("..")
    payload["rates"] = {day: r for day, r in payload["rates"].items() if day >= start}
    return payload


@dlt.source(name="frankfurter")
def frankfurter(
    base: str = "EUR",
    start_date: date | None = None,
    fetch: Fetch = fetch_api,
) -> list[DltResource]:
    """Currencies, and daily rates for ``base`` from ``start_date`` onwards.

    Rates load incrementally: each run asks only for days after the last one
    loaded, and merges on the natural key so re-runs never duplicate rows.
    """
    initial = start_date or date.today() - timedelta(days=30)

    @dlt.resource(write_disposition="replace")
    def currencies() -> Iterator[dict[str, str]]:
        for code, name in fetch("currencies", {}).items():
            yield {"code": code, "name": name}

    @dlt.resource(
        primary_key=("rate_date", "base_currency", "quote_currency"),
        write_disposition="merge",
    )
    def exchange_rates(
        # dlt injects the incremental state through this default.
        rate_date: incremental[date] = incremental(  # noqa: B008
            "rate_date", initial_value=initial
        ),
    ) -> Iterator[dict[str, Any]]:
        start = rate_date.last_value or initial
        payload = fetch(f"{start.isoformat()}..", {"base": base})
        for day, rates in payload["rates"].items():
            for quote, rate in rates.items():
                yield {
                    "rate_date": date.fromisoformat(day),
                    "base_currency": base,
                    "quote_currency": quote,
                    "rate": rate,
                }

    return [currencies, exchange_rates]
