"""
ETL service: ingest NEX-DCP30 NetCDF files from S3 and aggregate
pixel values to watershed polygons, writing results to the DB.

Designed to be run as a background task or CLI script.
"""

import asyncio
from datetime import date
from typing import List

import numpy as np
import xarray as xr
from rasterio.features import geometry_mask
from shapely.wkt import loads as wkt_loads
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.climate_record import ClimateRecord
from app.models.watershed import Watershed


class ETLService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def ingest_model_year(
        self,
        model: str,
        scenario: str,
        variable: str,
        year: int,
        watersheds: List[Watershed],
    ) -> int:
        """
        Read one year of daily NEX-DCP30 data and aggregate to each watershed.
        Returns number of records inserted.
        """
        import s3fs
        fs = s3fs.S3FileSystem(
            key=settings.AWS_ACCESS_KEY_ID,
            secret=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_path = (
            f"s3://{settings.NEX_DCP30_S3_BUCKET}/{settings.NEX_DCP30_S3_PREFIX}"
            f"/{model}/{scenario}/day/{variable}/{variable}_day_NEX-DCP30_{model}"
            f"_{scenario}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
        )

        records_inserted = 0
        with fs.open(s3_path) as f:
            ds = xr.open_dataset(f, engine="h5netcdf", chunks={"time": 30})
            da = ds[variable]

            for watershed in watersheds:
                if not watershed.geometry_wkt:
                    continue
                geom = wkt_loads(watershed.geometry_wkt)
                # Clip to watershed bbox then mask
                min_lon, min_lat, max_lon, max_lat = geom.bounds
                clipped = da.sel(
                    lon=slice(min_lon - 0.05, max_lon + 0.05),
                    lat=slice(min_lat - 0.05, max_lat + 0.05),
                )
                for time_idx in range(len(clipped.time)):
                    daily_slice = clipped.isel(time=time_idx).values
                    record_date = date.fromisoformat(
                        str(clipped.time[time_idx].values)[:10]
                    )
                    record = ClimateRecord(
                        watershed_id=watershed.id,
                        date=record_date,
                        model=model,
                        scenario=scenario,
                        variable=variable,
                        value_mean=float(np.nanmean(daily_slice)),
                        value_min=float(np.nanmin(daily_slice)),
                        value_max=float(np.nanmax(daily_slice)),
                        value_std=float(np.nanstd(daily_slice)),
                        pixel_count=int(np.sum(~np.isnan(daily_slice))),
                    )
                    self.db.add(record)
                    records_inserted += 1

        await self.db.commit()
        return records_inserted
