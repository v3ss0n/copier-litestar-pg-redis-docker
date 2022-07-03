from collections.abc import Awaitable
from typing import Any

from redis.asyncio import Redis
from starlite import CacheConfig
from starlite.config import CacheBackendProtocol

from app.config import cache_settings

redis = Redis.from_url(cache_settings.URL)


class RedisAsyncioBackend(CacheBackendProtocol):  # pragma: no cover
    async def get(  # pylint: disable=invalid-overridden-method
        self, key: str
    ) -> Awaitable[Any]:
        """
        Retrieve a valued from cache corresponding to the given key
        """
        return await redis.get(key)  # type:ignore[return-value]

    async def set(  # pylint:disable=invalid-overridden-method
        self, key: str, value: Any, expiration: int
    ) -> Awaitable[Any]:
        """
        Set a value in cache for a given key with a given expiration in seconds
        """
        return await redis.set(key, value, expiration)  # type:ignore[return-value]

    async def delete(  # pylint: disable=invalid-overridden-method
        self, key: str
    ) -> Awaitable[Any]:
        """
        Remove a value from the cache for a given key
        """
        return await redis.delete(key)  # type:ignore[return-value]


async def on_shutdown() -> None:
    """
    Passed to `Starlite.on_shutdown`.
    """
    await redis.close()


config = CacheConfig(backend=RedisAsyncioBackend())
