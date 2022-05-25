import asyncio
import sys

from sqlalchemy import text

from app.db import engine


async def c() -> None:
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Waiting for PostgreSQL: {e}")
        sys.exit(-1)
    else:
        print("Postgres OK!")


def main() -> None:
    asyncio.run(c())
