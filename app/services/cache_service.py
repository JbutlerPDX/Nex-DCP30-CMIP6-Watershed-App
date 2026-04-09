"""Redis-based caching service."""

import json
import pickle
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings


class CacheService:
    def __init__(self) -> None:
        self._client: Optional[aioredis.Redis] = None

    async def _get_client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.from_url(settings.REDIS_URL, decode_responses=False)
        return self._client

    async def get(self, key: str) -> Any:
        client = await self._get_client()
        value = await client.get(key)
        if value is None:
            return None
        return pickle.loads(value)

    async def set(self, key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS) -> None:
        client = await self._get_client()
        await client.set(key, pickle.dumps(value), ex=ttl)

    async def delete(self, key: str) -> None:
        client = await self._get_client()
        await client.delete(key)
