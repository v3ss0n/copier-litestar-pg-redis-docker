import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlite import Starlite
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from app import api, cache, db, exceptions, health, openapi
from app.config import app_settings, sentry_settings
from app.logging import log_config

sentry_sdk.init(
    dsn=sentry_settings.DSN,
    environment=app_settings.ENVIRONMENT,
    integrations=[SqlalchemyIntegration()],
    traces_sample_rate=sentry_settings.TRACES_SAMPLE_RATE,
)

app = Starlite(
    after_request=db.session_after_request,
    cache_config=cache.config,
    debug=app_settings.DEBUG,
    exception_handlers={
        HTTP_500_INTERNAL_SERVER_ERROR: exceptions.logging_exception_handler
    },
    middleware=[SentryAsgiMiddleware],
    on_shutdown=[db.on_shutdown, cache.on_shutdown],
    on_startup=[log_config.configure],
    openapi_config=openapi.config,
    plugins=[SQLAlchemyPlugin()],
    route_handlers=[health.check, api.v1_router],
)
