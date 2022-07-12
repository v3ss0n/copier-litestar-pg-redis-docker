from typing import Any

from sqlalchemy import text
from starlite import MediaType, get

from app.config import Paths, app_settings

from . import db


@get(path=Paths.HEALTH, media_type=MediaType.JSON, cache=False, tags=["Misc"])
async def health_check() -> dict[str, Any]:
    """Health check handler"""
    assert (await db.AsyncScopedSession().execute(text("SELECT 1"))).scalar_one() == 1
    return {"app": app_settings.NAME, "build": app_settings.BUILD_NUMBER}
