from sqlalchemy import text
from starlite import MediaType, get

from app.config import Paths

from . import db


@get(path=Paths.HEALTH, media_type=MediaType.TEXT, cache=False, tags=["Misc"])
async def health_check() -> str:
    """Health check handler"""
    assert (await db.AsyncScopedSession().execute(text("SELECT 1"))).scalar_one() == 1
    return "OK"
