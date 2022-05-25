import asyncio
import sys

from redis.asyncio import Redis

from app.config import cache_settings


async def c() -> None:
    redis = Redis.from_url(cache_settings.URL)
    try:
        await redis.ping()
    except Exception as e:
        print(f"Waiting  for Redis: {e}")
        sys.exit(-1)
    else:
        print("Redis OK!")
    finally:
        await redis.close()


def main() -> None:
    asyncio.run(c())
