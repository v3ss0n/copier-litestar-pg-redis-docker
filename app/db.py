from typing import TYPE_CHECKING, cast

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import settings

if TYPE_CHECKING:
    from starlite.datastructures import State


def get_postgres_connection(state: "State") -> AsyncEngine:
    """
    Returns the Postgres connection stored in the application state, if it doesn't exist, creates it first.

    This function is called during startup and is also injected as a dependency.
    """
    if not hasattr(state, "postgres_connection"):
        state.postgres_connection = create_async_engine(settings.DATABASE_URI)
    return cast(AsyncEngine, state.postgres_connection)


async def close_postgres_connection(state: "State") -> None:
    """
    Closes the postgres connection stored in the application state. This function is called during shutdown.
    """
    if hasattr(state, "postgres_connection"):
        engine = cast(AsyncEngine, state.postgres_connection)
        await engine.dispose()
