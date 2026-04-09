"""
CLI script to ingest NEX-DCP30 data for a given model/scenario/variable/year range.

Usage:
    python scripts/ingest_nexdcp30.py \
        --model CESM2 --scenario ssp245 --variable tasmax \
        --start-year 2025 --end-year 2035
"""

import asyncio
import argparse

from app.db.session import async_session_factory
from app.services.etl_service import ETLService
from app.services.watershed_service import WatershedService


async def main(model: str, scenario: str, variable: str, start_year: int, end_year: int):
    async with async_session_factory() as db:
        watershed_svc = WatershedService(db=db)
        watersheds_resp = await watershed_svc.list_watersheds()
        from sqlalchemy import select
        from app.models.watershed import Watershed
        result = await db.execute(select(Watershed))
        watersheds = result.scalars().all()

        etl = ETLService(db=db)
        for year in range(start_year, end_year + 1):
            n = await etl.ingest_model_year(model, scenario, variable, year, watersheds)
            print(f"  {year}: inserted {n} records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--variable", required=True)
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    args = parser.parse_args()
    asyncio.run(main(args.model, args.scenario, args.variable, args.start_year, args.end_year))
