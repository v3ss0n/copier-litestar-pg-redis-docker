from typing import cast

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlite.datastructures import State

from app.config import settings


def get_postgres_connection(state: State) -> AsyncEngine:
    """
    Returns the Postgres connection stored in the application state, if it doesn't exist, creates it first.

    This function is called during startup and is also injected as a dependency.
    """
    if not hasattr(state, "postgres_connection"):
        state.postgres_connection = create_async_engine(settings.DATABASE_URI)
    return cast(AsyncEngine, state.postgres_connection)


async def close_postgres_connection(state: State) -> None:
    """
    Closes the postgres connection stored in the application state. This function is called during shutdown.
    """
    if hasattr(state, "postgres_connection"):
        engine = cast(AsyncEngine, state.postgres_connection)
        await engine.dispose()


def create_async_session(state: State) -> AsyncSession:
    """
    Creates a sessionmaler from the given connection
    """
    if hasattr(state, "postgres_connection"):
        postgres_connection = cast(AsyncEngine, state.postgres_connection)
        return sessionmaker(postgres_connection, class_=AsyncSession, expire_on_commit=False)()
    raise RuntimeError("postgres_connection has not been set in state")
