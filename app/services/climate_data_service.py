"""
Service layer for NEX-DCP30 climate data retrieval and aggregation.

Reads from:
  1. Pre-aggregated database records (fast path for time-series queries)
  2. S3/NetCDF files via xarray + s3fs (for on-demand spatial queries)
"""

from datetime import date
from typing import List, Optional

import numpy as np
import xarray as xr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.climate_record import ClimateRecord
from app.models.watershed import Watershed
from app.schemas.climate import ClimateDataPoint, EnsembleStatistics
from app.services.cache_service import CacheService


VARIABLE_UNITS = {"tasmax": "K", "tasmin": "K", "pr": "kg m-2 s-1"}


class ClimateDataService:
    def __init__(self, db: AsyncSession, cache: CacheService) -> None:
        self.db = db
        self.cache = cache

    # ------------------------------------------------------------------
    # Time-series: reads from pre-aggregated DB table
    # ------------------------------------------------------------------

    async def get_time_series(
        self,
        huc_code: str,
        variable: str,
        scenario: str,
        start_date: date,
        end_date: date,
        models: Optional[List[str]] = None,
    ) -> List[ClimateDataPoint]:
        cache_key = f"ts:{huc_code}:{variable}:{scenario}:{start_date}:{end_date}"
        if cached := await self.cache.get(cache_key):
            return cached

        stmt = (
            select(ClimateRecord)
            .join(Watershed)
            .where(
                Watershed.huc_code == huc_code,
                ClimateRecord.variable == variable,
                ClimateRecord.scenario == scenario,
                ClimateRecord.date >= start_date,
                ClimateRecord.date <= end_date,
            )
        )
        if models:
            stmt = stmt.where(ClimateRecord.model.in_(models))

        result = await self.db.execute(stmt)
        records = result.scalars().all()

        data = [
            ClimateDataPoint(
                date=r.date,
                model=r.model,
                value_mean=r.value_mean,
                value_min=r.value_min,
                value_max=r.value_max,
                value_std=r.value_std,
            )
            for r in records
        ]
        await self.cache.set(cache_key, data)
        return data

    # ------------------------------------------------------------------
    # Ensemble statistics across models
    # ------------------------------------------------------------------

    async def get_ensemble_statistics(
        self,
        huc_code: str,
        variable: str,
        scenario: str,
        start_date: date,
        end_date: date,
    ) -> List[EnsembleStatistics]:
        raw = await self.get_time_series(huc_code, variable, scenario, start_date, end_date)

        from collections import defaultdict
        daily: dict = defaultdict(list)
        for pt in raw:
            daily[pt.date].append(pt.value_mean)

        return [
            EnsembleStatistics(
                date=d,
                ensemble_mean=float(np.mean(vals)),
                ensemble_p10=float(np.percentile(vals, 10)),
                ensemble_p90=float(np.percentile(vals, 90)),
                model_count=len(vals),
            )
            for d, vals in sorted(daily.items())
        ]

    # ------------------------------------------------------------------
    # Spatial / raster: reads directly from S3 NetCDF via xarray
    # ------------------------------------------------------------------

    def _s3_path(self, model: str, scenario: str, variable: str, year: int) -> str:
        return (
            f"s3://{settings.NEX_DCP30_S3_BUCKET}/{settings.NEX_DCP30_S3_PREFIX}"
            f"/{model}/{scenario}/day/{variable}/{variable}_day_NEX-DCP30_{model}"
            f"_{scenario}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
        )

    async def get_spatial_slice(
        self,
        model: str,
        scenario: str,
        variable: str,
        target_date: date,
        bbox: tuple,  # (min_lon, min_lat, max_lon, max_lat)
    ) -> xr.DataArray:
        import s3fs
        fs = s3fs.S3FileSystem(
            key=settings.AWS_ACCESS_KEY_ID,
            secret=settings.AWS_SECRET_ACCESS_KEY,
        )
        path = self._s3_path(model, scenario, variable, target_date.year)
        with fs.open(path) as f:
            ds = xr.open_dataset(f, engine="h5netcdf")
            da = ds[variable].sel(time=str(target_date), method="nearest")
            min_lon, min_lat, max_lon, max_lat = bbox
            da = da.sel(lon=slice(min_lon, max_lon), lat=slice(min_lat, max_lat))
        return da
