import sentry_sdk

from src.configs.sentry import sentry_config


def init_sentry():
    """Инициализировать отправку ошибок в sentry."""
    if sentry_config.enabled:
        sentry_sdk.init(
            dsn=sentry_config.dsn,
            traces_sample_rate=sentry_config.traces_sample_rate
        )
