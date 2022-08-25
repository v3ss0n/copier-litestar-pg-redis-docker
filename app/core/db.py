import json
from asyncio import current_task
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from starlite import Response

from app.settings import db_settings


def _default(val: Any) -> str:
    if isinstance(val, UUID):
        return str(val)
    raise TypeError()


def dumps(d: dict[str, Any]) -> str:
    """Alternate JSON serializer for sqlalchemy queries.

    Parameters
    ----------
    d : dict[str, Any]

    Returns
    -------
    str
    """
    return json.dumps(d, default=_default)


engine = create_async_engine(db_settings.URL, echo=db_settings.ECHO, json_serializer=dumps)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


async def on_shutdown() -> None:
    """Passed to `Starlite.on_shutdown`."""
    await engine.dispose()


async def session_after_request(response: Response) -> Response:
    """Passed to `Starlite.after_request`.

    Inspects `response` to determine if we should commit, or rollback the database
    transaction.

    Finally, calls `remove()` on the scoped session.

    Parameters
    ----------
    response : Response

    Returns
    -------
    Response
    """
    if 200 <= response.status_code < 300:
        await AsyncScopedSession.commit()
    else:
        await AsyncScopedSession.rollback()
    await AsyncScopedSession.remove()
    return response
