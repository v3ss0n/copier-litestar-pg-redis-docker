from starlite import Starlite
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from app import api, cache, db, health, openapi
from app.config import app_settings, log_config

app = Starlite(
    after_request=db.session_after_request,
    cache_config=cache.config,
    debug=app_settings.DEBUG,
    on_shutdown=[db.on_shutdown, cache.on_shutdown],
    on_startup=[log_config.configure],
    openapi_config=openapi.config,
    plugins=[SQLAlchemyPlugin()],
    route_handlers=[health.check, api.v1_router],
)
