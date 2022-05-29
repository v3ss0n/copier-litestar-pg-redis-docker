from sqlalchemy import text
from starlite import MediaType, OpenAPIConfig, Starlite, get
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from app import api, cache, db
from app.config import Paths, app_settings, log_config


@get(path=Paths.HEALTH, media_type=MediaType.TEXT, cache=False)
async def health_check() -> str:
    assert (await db.AsyncScopedSession().execute(text("SELECT 1"))).scalar_one() == 1
    return "OK"


app = Starlite(
    after_request=db.session_after_request,
    cache_config=cache.config,
    debug=app_settings.DEBUG,
    on_shutdown=[db.on_shutdown, cache.on_shutdown],
    on_startup=[log_config.configure],
    openapi_config=OpenAPIConfig(
        title="Starlite Postgres Example API", version="1.0.0"
    ),
    plugins=[SQLAlchemyPlugin()],
    route_handlers=[health_check, api.v1_router],
)
