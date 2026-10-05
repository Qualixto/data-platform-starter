import argparse
from datetime import date

import duckdb

from data_platform_starter.pipeline import ingest, warehouse_path
from data_platform_starter.transform import dbt, product_schema


def summary() -> str:
    """Describe the FX product: row count, latest date and a few headline rates."""
    with duckdb.connect(str(warehouse_path())) as con:
        table = f"{product_schema()}.fx_rates_gbp"
        count, latest = con.execute(
            f"select count(*), max(rate_date) from {table}"  # noqa: S608
        ).fetchone() or (0, None)
        rates = con.execute(
            f"select currency_code, rate_per_gbp from {table}"  # noqa: S608
            " where rate_date = ? and currency_code in ('EUR', 'USD', 'JPY')"
            " order by currency_code",
            [latest],
        ).fetchall()
    headline = ", ".join(f"{code} {rate:.4f}" for code, rate in rates)
    return f"fx_rates_gbp: {count} rows, latest {latest}. 1 GBP = {headline}"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the data platform locally.")
    commands = parser.add_subparsers(dest="command", required=True)
    ingest_cmd = commands.add_parser("ingest", help="Load raw data with dlt")
    ingest_cmd.add_argument(
        "--fixtures", action="store_true", default=None, help="Use offline data"
    )
    ingest_cmd.add_argument("--start-date", type=date.fromisoformat)
    commands.add_parser("build", help="Build and test all dbt models")
    commands.add_parser("demo", help="Ingest fixtures, build, and summarise")
    args = parser.parse_args(argv)

    if args.command == "ingest":
        print(ingest(fixtures=args.fixtures, start_date=args.start_date))
    elif args.command == "build":
        dbt("build")
    else:
        ingest(fixtures=True)
        dbt("build")
        print(summary())


if __name__ == "__main__":
    main()
