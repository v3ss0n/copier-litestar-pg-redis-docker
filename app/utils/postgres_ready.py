import asyncio
import sys

from sqlalchemy import text

from app.db import engine


async def c() -> None:
    """
    Database connectivity test.
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:  # pylint: disable=broad-except
        print(f"Waiting for PostgreSQL: {e}")  # noqa: T201
        sys.exit(-1)
    else:
        print("Postgres OK!")  # noqa: T201


def main() -> None:
    """
    Wraps async entrypoint.
    """
    asyncio.run(c())
