"""Pydantic schemas for climate data request/response."""

from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ClimateQueryParams(BaseModel):
    huc_code: str = Field(..., description="HUC watershed code")
    variable: str = Field(..., description="Climate variable: tasmax | tasmin | pr")
    scenario: str = Field("ssp245", description="SSP scenario or 'historical'")
    models: Optional[List[str]] = Field(None, description="Specific models; None = all")
    start_date: date = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: date = Field(..., description="End date (YYYY-MM-DD)")


class ClimateDataPoint(BaseModel):
    date: date
    model: str
    value_mean: float
    value_min: Optional[float]
    value_max: Optional[float]
    value_std: Optional[float]


class EnsembleStatistics(BaseModel):
    date: date
    ensemble_mean: float
    ensemble_p10: float
    ensemble_p90: float
    model_count: int


class ClimateTimeSeriesResponse(BaseModel):
    huc_code: str
    variable: str
    scenario: str
    unit: str
    data: List[ClimateDataPoint]


class EnsembleTimeSeriesResponse(BaseModel):
    huc_code: str
    variable: str
    scenario: str
    unit: str
    ensemble: List[EnsembleStatistics]


class ClimateSpatialResponse(BaseModel):
    """GeoJSON FeatureCollection with climate values per watershed pixel."""
    type: str = "FeatureCollection"
    variable: str
    date: date
    model: str
    scenario: str
    features: List[Dict]
