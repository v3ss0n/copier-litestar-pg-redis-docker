from pydantic import AnyUrl, BaseSettings, PostgresDsn
from starlite import LoggingConfig


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    DEBUG: bool
    DEFAULT_PAGINATION_LIMIT: int


class CacheSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"
        case_sensitive = True

    URL: AnyUrl


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = True

    ECHO: bool
    URL: PostgresDsn


class GunicornSettings(BaseSettings):
    class Config:
        case_sensitive = True
        env_prefix = "GUNICORN_"

    ACCESS_LOG: str
    ERROR_LOG: str
    HOST: str
    KEEPALIVE: int
    LOG_LEVEL: str
    PORT: int
    RELOAD: str
    THREADS: int
    TIMEOUT: int
    WORKERS: int
    WORKER_CLASS: str


# Constants
class Paths:
    HEALTH = "/health"
    V1 = "/v1"
    USERS = "/users"
    ITEMS = f"{USERS}/{{user_id:uuid}}/items"


app_settings = AppSettings()
cache_settings = CacheSettings()
db_settings = DatabaseSettings()
gunicorn_settings = GunicornSettings()

log_config = LoggingConfig(
    loggers={
        "app": {"level": "INFO", "handlers": ["queue_listener"], "propagate": False}
    }
)
