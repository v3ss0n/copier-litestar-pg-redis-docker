from typing import cast

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from starlette.datastructures import State

from app.config import settings

state = State()


def get_postgres_connection() -> AsyncEngine:
    """Returns the Postgres connection. If it doesn't exist, creates it and saves it in a State object"""
    if not state.get("postgres_connection"):
        state["postgres_connection"] = create_async_engine(settings.DATABASE_URI, echo=True, pool_pre_ping=True)
    return cast(AsyncEngine, state.get("postgres_connection"))


async def close_postgres_connection() -> None:
    """Closes the postgres connection stored in the given State object"""
    engine = state.get("postgres_connection")
    if engine:
        await cast(AsyncEngine, engine).dispose()
