from starlite import LoggingConfig, MediaType, OpenAPIConfig, Starlite, get
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from app.api import v1_router
from app.config import app_settings
from app.constants import MESSAGE_HEALTHY
from app.db import dispose_engine, session_after_request


@get(path="/health-check", media_type=MediaType.TEXT)
def health_check() -> str:
    return MESSAGE_HEALTHY


logger = LoggingConfig(loggers={"app": {"level": "DEBUG", "handlers": ["console"]}})

app = Starlite(
    debug=app_settings.DEBUG,
    on_shutdown=[dispose_engine],
    # on_startup=[logger.configure],
    openapi_config=OpenAPIConfig(
        title="Starlite Postgres Example API", version="1.0.0"
    ),
    plugins=[SQLAlchemyPlugin()],
    route_handlers=[health_check, v1_router],
    after_request=session_after_request,
)
