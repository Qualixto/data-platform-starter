import argparse

from data_platform_starter.core import greet


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="A runnable baseline data platform: dlt, DuckDB/MotherDuck, dbt and Dagster, with data contracts, quality gates and CI")
    parser.add_argument("name", nargs="?", default="world")
    args = parser.parse_args(argv)
    print(greet(args.name))


if __name__ == "__main__":
    main()
