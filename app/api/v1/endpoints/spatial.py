"""Spatial (raster/pixel-level) climate endpoints."""

from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.core.config import settings
from app.core.dependencies import get_climate_service
from app.services.climate_data_service import ClimateDataService

router = APIRouter()


@router.get("/slice")
async def get_spatial_slice(
    model: str = Query(...),
    scenario: str = Query("ssp245"),
    variable: str = Query(...),
    target_date: date = Query(...),
    min_lon: float = Query(...),
    min_lat: float = Query(...),
    max_lon: float = Query(...),
    max_lat: float = Query(...),
    service: ClimateDataService = Depends(get_climate_service),
):
    """
    Return a NetCDF spatial slice for a bounding box on a given date.
    Useful for map tile generation or frontend raster display.
    """
    da = await service.get_spatial_slice(
        model=model,
        scenario=scenario,
        variable=variable,
        target_date=target_date,
        bbox=(min_lon, min_lat, max_lon, max_lat),
    )
    nc_bytes = da.to_netcdf()
    return Response(content=nc_bytes, media_type="application/x-netcdf4")
