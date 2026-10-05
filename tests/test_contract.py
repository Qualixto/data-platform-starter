"""The ODCS contract and the enforced dbt contract must describe the same table."""

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parent.parent


def load(path: str) -> Any:
    return yaml.safe_load((ROOT / path).read_text())


def test_odcs_contract_matches_dbt_model_contract() -> None:
    odcs = load("contracts/fx_rates_gbp.odcs.yaml")["schema"][0]["properties"]
    model = load("dbt/models/products/_products__models.yml")["models"][0]

    contract = {p["name"]: (p["physicalType"], p["required"]) for p in odcs}
    dbt_columns = {
        c["name"]: (
            c["data_type"],
            any(k["type"] == "not_null" for k in c.get("constraints", [])),
        )
        for c in model["columns"]
    }

    assert contract == dbt_columns


def test_dbt_model_points_at_its_contract() -> None:
    model = load("dbt/models/products/_products__models.yml")["models"][0]
    path = model["config"]["meta"]["contract"]

    assert load(path)["schema"][0]["name"] == model["name"]
