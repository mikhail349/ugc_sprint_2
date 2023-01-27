from flask import Flask
import redis

from src.configs.redis import redis_config
from src.cache.redis import Redis


def init_cache(app: Flask) -> None:
    """Инициализировать кэш.

    Args:
        app: приложение Flask.

    """
    redis_cache = redis.Redis(
        host=redis_config.host,
        port=redis_config.port,
        db=redis_config.db
    )

    app.config['cache'] = Redis(
        redis=redis_cache,
        cache_expires=redis_config.cache_expires
    )
