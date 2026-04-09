"""Watershed boundary endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.dependencies import get_watershed_service
from app.schemas.watershed import WatershedGeoJSONResponse, WatershedResponse
from app.services.watershed_service import WatershedService

router = APIRouter()


@router.get("/", response_model=List[WatershedResponse])
async def list_watersheds(
    huc_level: Optional[int] = Query(None, ge=4, le=12, description="Filter by HUC level"),
    service: WatershedService = Depends(get_watershed_service),
):
    """List all available watersheds, optionally filtered by HUC level."""
    return await service.list_watersheds(huc_level=huc_level)


@router.get("/{huc_code}", response_model=WatershedResponse)
async def get_watershed(
    huc_code: str,
    service: WatershedService = Depends(get_watershed_service),
):
    """Get watershed metadata by HUC code."""
    watershed = await service.get_by_huc(huc_code)
    if not watershed:
        raise HTTPException(status_code=404, detail=f"Watershed {huc_code} not found")
    return watershed


@router.get("/{huc_code}/geojson", response_model=WatershedGeoJSONResponse)
async def get_watershed_geojson(
    huc_code: str,
    service: WatershedService = Depends(get_watershed_service),
):
    """Get watershed as a GeoJSON Feature."""
    geojson = await service.get_geojson(huc_code)
    if not geojson:
        raise HTTPException(status_code=404, detail=f"Watershed {huc_code} not found")
    return geojson
