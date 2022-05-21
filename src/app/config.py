from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    DEBUG: bool


class CacheSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"
        case_sensitive = True

    URL: str


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = True

    DB: str
    PASSWORD: str
    SERVER: str
    USER: str

    @property
    def async_database_uri(self) -> PostgresDsn:
        return PostgresDsn.build(  # type:ignore[no-any-return]
            scheme="postgresql+asyncpg",
            user=self.USER,
            password=self.PASSWORD,
            host=self.SERVER,
            path=f"/{self.DB}",
        )

    @property
    def sync_database_uri(self) -> PostgresDsn:
        return PostgresDsn.build(  # type:ignore[no-any-return]
            scheme="postgresql",
            user=self.USER,
            password=self.PASSWORD,
            host=self.SERVER,
            path=f"/{self.DB}",
        )


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


app_settings = AppSettings()
cache_settings = CacheSettings()
db_settings = DatabaseSettings()
gunicorn_settings = GunicornSettings()
