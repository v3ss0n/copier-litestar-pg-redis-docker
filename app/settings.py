from pydantic import BaseSettings, PostgresDsn, RedisDsn


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    BUILD_NUMBER: str
    DEBUG: bool
    DEFAULT_PAGINATION_LIMIT: int
    ENVIRONMENT: str
    LOG_LEVEL: str
    NAME: str

    @property
    def slug(self) -> str:
        """Name without spaces and all lower case."""
        return "-".join(self.NAME.lower().split())


class CacheSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"
        case_sensitive = True

    EXPIRATION: int
    URL: RedisDsn


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = True

    ECHO: bool
    URL: PostgresDsn


class ServerSettings(BaseSettings):
    class Config:
        case_sensitive = True
        env_prefix = "UVICORN_"

    HOST: str
    KEEPALIVE: int
    LOG_LEVEL: str
    PORT: int
    RELOAD: str
    TIMEOUT: int


class SentrySettings(BaseSettings):
    class Config:
        env_prefix = "SENTRY_"
        case_sensitive = True

    DSN: str
    TRACES_SAMPLE_RATE: float


app_settings = AppSettings()
cache_settings = CacheSettings()
db_settings = DatabaseSettings()
server_settings = ServerSettings()
sentry_settings = SentrySettings()
