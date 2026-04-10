"""Application configuration via environment variables."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    SECRET_KEY: str = "dev-secret-key"
    API_V1_PREFIX: str = "/api/v1"

    # Database (PostGIS recommended)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/nex_watershed"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600

    # AWS / S3 access to NEX-DCP30
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-west-2"
    NEX_DCP30_S3_BUCKET: str = "bdt-nex-dcp30-cmip6"
    NEX_DCP30_S3_PREFIX: str = "NEX-DCP30/NEX-DCP30-5BCMIP6"

    # NEX-DCP30 domain settings
    DEFAULT_SCENARIO: str = "ssp245"
    SUPPORTED_SCENARIOS: List[str] = ["historical","ssp126","ssp245","ssp370", "ssp585"]
    SUPPORTED_VARIABLES: List[str] = ["tasmax", "tasmin", "pr"]
    SUPPORTED_MODELS: List[str] = [
        "ACCESS-CM2", "CESM2", "CNRM-CM6-1", "EC-Earth3",
        "GFDL-ESM4", "INM-CM5-0", "IPSL-CM6A-LR", "MIROC6",
        "MPI-ESM1-2-HR", "MRI-ESM2-0", "NorESM2-MM",
    ]

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
