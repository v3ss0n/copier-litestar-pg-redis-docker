from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from starlite import Response

from app.config import db_settings

engine = create_async_engine(db_settings.URL, echo=db_settings.ECHO)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


async def on_shutdown() -> None:
    """
    Passed to `Starlite.on_shutdown`.
    """
    await engine.dispose()


async def session_after_request(response: Response) -> Response:
    """
    Passed to `Starlite.after_request`.

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
