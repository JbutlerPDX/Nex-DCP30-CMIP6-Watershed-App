"""Service layer for watershed boundary operations."""

import json
from typing import List, Optional

from shapely.geometry import mapping, shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.watershed import Watershed
from app.schemas.watershed import WatershedGeoJSONResponse, WatershedResponse


class WatershedService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_huc(self, huc_code: str) -> Optional[Watershed]:
        result = await self.db.execute(
            select(Watershed).where(Watershed.huc_code == huc_code)
        )
        return result.scalar_one_or_none()

    async def list_watersheds(self, huc_level: Optional[int] = None) -> List[WatershedResponse]:
        stmt = select(Watershed)
        if huc_level:
            stmt = stmt.where(Watershed.huc_level == huc_level)
        result = await self.db.execute(stmt)
        return [WatershedResponse.model_validate(w) for w in result.scalars().all()]

    async def get_geojson(self, huc_code: str) -> Optional[WatershedGeoJSONResponse]:
        watershed = await self.get_by_huc(huc_code)
        if not watershed or not watershed.geometry_wkt:
            return None
        from shapely.wkt import loads
        geom = loads(watershed.geometry_wkt)
        return WatershedGeoJSONResponse(
            properties={
                "huc_code": watershed.huc_code,
                "name": watershed.name,
                "area_sq_km": watershed.area_sq_km,
            },
            geometry=mapping(geom),
        )
