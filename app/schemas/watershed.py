"""Pydantic schemas for watershed request/response."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class WatershedBase(BaseModel):
    huc_code: str = Field(..., description="HUC code (4, 8, or 12 digit)")
    name: str
    huc_level: int = Field(..., ge=4, le=12)
    area_sq_km: Optional[float] = None
    centroid_lat: Optional[float] = None
    centroid_lon: Optional[float] = None


class WatershedResponse(WatershedBase):
    id: int
    model_config = {"from_attributes": True}


class WatershedGeoJSONResponse(BaseModel):
    type: str = "Feature"
    properties: Dict[str, Any]
    geometry: Dict[str, Any]
