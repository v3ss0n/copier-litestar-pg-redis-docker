from sqlalchemy import text
from starlite import MediaType, get

from app import db
from app.config import Paths


@get(
    path=Paths.HEALTH,
    media_type=MediaType.TEXT,
    cache=False,
    tags=["Misc"],
    operation_id="Health Check",
)
async def check() -> str:
    """
    Checks database connection.
    """
    assert (await db.AsyncScopedSession().execute(text("SELECT 1"))).scalar_one() == 1
    return "OK"
