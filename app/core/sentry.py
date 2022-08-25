import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.settings import app_settings, sentry_settings


def on_startup() -> None:
    """Callback to configure sentry on app startup."""
    sentry_sdk.init(
        dsn=sentry_settings.DSN,
        environment=app_settings.ENVIRONMENT,
        release=app_settings.BUILD_NUMBER,
        integrations=[SqlalchemyIntegration()],
        traces_sample_rate=sentry_settings.TRACES_SAMPLE_RATE,
    )
