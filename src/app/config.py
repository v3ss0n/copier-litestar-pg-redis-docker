from pydantic import BaseSettings
from sqlalchemy.engine import URL


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

    DRIVERNAME: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    DATABASE: str

    @property
    def database_uri(self) -> URL:
        """
        For async connections to db.

            >>> db_conf = DatabaseSettings(
            ...     DRIVERNAME="postgresql+asyncpg",
            ...     USERNAME="postgres",
            ...     PASSWORD="mysecretpassword",
            ...     HOST="db",
            ...     PORT=5432,
            ...     DATABASE="example-pg-docker",
            ... )
            >>> db_conf.database_uri
            postgresql+asyncpg://postgres:***@db:5432/example-pg-docker

        Returns
        -------
        URL
        """
        return URL.create(
            drivername=self.DRIVERNAME,
            username=self.USERNAME,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.DATABASE,
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
