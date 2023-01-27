from pydantic import Field, Required
from src.configs.base import BaseConfig


class SentryConfig(BaseConfig):
    """Настройки Sentry."""

    dsn: str = Field(Required, env="SENTRY_DSN")
    traces_sample_rate: float = Field(1.0, env="SENTRY_TRACES_SAMPLE_RATE")
    enabled: bool = Field(False, env="SENTRY_ENABLED")


sentry_config = SentryConfig()
