"""Top-level API v1 router."""

from fastapi import APIRouter
from app.api.v1.endpoints import health, watersheds, climate, ensemble, spatial

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(watersheds.router, prefix="/watersheds", tags=["Watersheds"])
api_router.include_router(climate.router, prefix="/climate", tags=["Climate Data"])
api_router.include_router(ensemble.router, prefix="/ensemble", tags=["Ensemble"])
api_router.include_router(spatial.router, prefix="/spatial", tags=["Spatial"])
