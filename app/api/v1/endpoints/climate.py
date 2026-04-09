"""Per-model climate time-series endpoints."""

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import settings
from app.core.dependencies import get_climate_service
from app.schemas.climate import ClimateTimeSeriesResponse
from app.services.climate_data_service import ClimateDataService, VARIABLE_UNITS

router = APIRouter()


@router.get("/timeseries", response_model=ClimateTimeSeriesResponse)
async def get_climate_timeseries(
    huc_code: str = Query(..., description="HUC watershed code"),
    variable: str = Query(..., description="tasmax | tasmin | pr"),
    scenario: str = Query("ssp245", description="historical | ssp245 | ssp585"),
    models: Optional[List[str]] = Query(None, description="Model filter"),
    start_date: date = Query(...),
    end_date: date = Query(...),
    service: ClimateDataService = Depends(get_climate_service),
):
    if variable not in settings.SUPPORTED_VARIABLES:
        raise HTTPException(400, f"Unsupported variable. Choose from {settings.SUPPORTED_VARIABLES}")
    if scenario not in settings.SUPPORTED_SCENARIOS:
        raise HTTPException(400, f"Unsupported scenario. Choose from {settings.SUPPORTED_SCENARIOS}")

    data = await service.get_time_series(
        huc_code=huc_code,
        variable=variable,
        scenario=scenario,
        start_date=start_date,
        end_date=end_date,
        models=models,
    )
    return ClimateTimeSeriesResponse(
        huc_code=huc_code,
        variable=variable,
        scenario=scenario,
        unit=VARIABLE_UNITS.get(variable, ""),
        data=data,
    )
