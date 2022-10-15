import contextlib

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlite import get
from starlite.exceptions import ServiceUnavailableException

from . import settings
from .settings import AppSettings


class HealthCheckFailure(ServiceUnavailableException):
    """Raise for health check failure."""


@get(path=settings.api.HEALTH_PATH, cache=False, tags=["Misc"])
async def health_check(db_session: AsyncSession) -> AppSettings:
    """Check database available and returns app config info."""
    with contextlib.suppress(Exception):
        if (await db_session.execute(text("SELECT 1"))).scalar_one() == 1:
            return settings.app
    raise HealthCheckFailure("DB not ready.")
