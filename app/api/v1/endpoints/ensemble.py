"""Multi-model ensemble statistics endpoints."""

from datetime import date
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_climate_service
from app.schemas.climate import EnsembleTimeSeriesResponse
from app.services.climate_data_service import ClimateDataService, VARIABLE_UNITS

router = APIRouter()


@router.get("/timeseries", response_model=EnsembleTimeSeriesResponse)
async def get_ensemble_timeseries(
    huc_code: str = Query(...),
    variable: str = Query(...),
    scenario: str = Query("ssp245"),
    start_date: date = Query(...),
    end_date: date = Query(...),
    service: ClimateDataService = Depends(get_climate_service),
):
    """Return ensemble mean, p10, and p90 across all available models."""
    ensemble = await service.get_ensemble_statistics(
        huc_code=huc_code,
        variable=variable,
        scenario=scenario,
        start_date=start_date,
        end_date=end_date,
    )
    return EnsembleTimeSeriesResponse(
        huc_code=huc_code,
        variable=variable,
        scenario=scenario,
        unit=VARIABLE_UNITS.get(variable, ""),
        ensemble=ensemble,
    )
