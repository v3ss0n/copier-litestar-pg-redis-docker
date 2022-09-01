from redis.asyncio import Redis
from starlite import CacheConfig
from starlite.config.cache import default_cache_key_builder
from starlite.connection import Request

from app.settings import app_settings, cache_settings

redis = Redis.from_url(cache_settings.URL)


def cache_key_builder(request: Request) -> str:
    """
    App name prefixed cache key builder.
    Parameters
    ----------
    request : Request
        Current request instance.
    Returns
    -------
    str
        App slug prefixed cache key.
    """
    return f"{app_settings.slug}:{default_cache_key_builder(request)}"


config = CacheConfig(
    backend=redis,
    expiration=cache_settings.EXPIRATION,
    cache_key_builder=cache_key_builder,
)
"""Cache configuration for application."""
