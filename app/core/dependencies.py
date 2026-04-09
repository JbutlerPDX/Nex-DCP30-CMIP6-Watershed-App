"""FastAPI dependency injection providers."""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.services.cache_service import CacheService
from app.services.climate_data_service import ClimateDataService
from app.services.watershed_service import WatershedService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_cache_service() -> CacheService:
    return CacheService()


async def get_climate_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service),
) -> ClimateDataService:
    return ClimateDataService(db=db, cache=cache)


async def get_watershed_service(
    db: AsyncSession = Depends(get_db),
) -> WatershedService:
    return WatershedService(db=db)
