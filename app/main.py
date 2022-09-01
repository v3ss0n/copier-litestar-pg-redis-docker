from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlite import CompressionConfig, Starlite

from app import domain
from app.core import cache, client, db, exceptions, response, routes, sentry
from app.core.logging import log_config
from app.settings import app_settings

app = Starlite(
    after_request=db.session_after_request,
    cache_config=cache.config,
    debug=app_settings.DEBUG,
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exceptions.logging_exception_handler},
    compression_config=CompressionConfig(backend="gzip"),
    on_shutdown=[db.on_shutdown, cache.redis.close, client.on_shutdown],
    on_startup=[log_config.configure, sentry.on_startup],
    # openapi_config=openapi.config,
    openapi_config=None,
    response_class=response.Response,
    route_handlers=[routes.health_check, domain.router],
)
