"""Ingestion entrypoint: python -m dispatch.ingest.run --months 24"""
from __future__ import annotations

import argparse
import logging

from dispatch import db
from dispatch.ingest.aemo import ingest_prices
from dispatch.ingest.weather import ingest_weather

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", type=int, default=24, help="months of history")
    args = parser.parse_args()

    prices = ingest_prices(months_back=args.months)
    weather = ingest_weather(months_back=args.months)
    db.rebuild()
    print(
        f"Ingest complete: {len(prices):,} price rows, "
        f"{len(weather):,} weather rows -> data/dispatch.duckdb"
    )


if __name__ == "__main__":
    main()
