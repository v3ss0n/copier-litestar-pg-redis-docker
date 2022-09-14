import uvicorn
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlite import CompressionConfig, Starlite

from app import domain
from app.core import (
    cache,
    client,
    db,
    exceptions,
    openapi,
    response,
    routes,
    sentry,
    static_files,
)
from app.core.logging import log_config
from app.settings import app_settings, server_settings

app = Starlite(
    after_request=db.session_after_request,
    cache_config=cache.config,
    debug=app_settings.DEBUG,
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exceptions.logging_exception_handler},
    compression_config=CompressionConfig(backend="gzip"),
    on_shutdown=[db.on_shutdown, cache.redis.close, client.on_shutdown],
    on_startup=[log_config.configure, sentry.on_startup],
    openapi_config=openapi.config,
    response_class=response.Response,
    route_handlers=[routes.health_check, domain.router],
    static_files_config=static_files.config,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=server_settings.HOST,
        log_level=server_settings.LOG_LEVEL,
        port=server_settings.PORT,
        reload=server_settings.RELOAD,
        timeout_keep_alive=server_settings.KEEPALIVE,
    )
