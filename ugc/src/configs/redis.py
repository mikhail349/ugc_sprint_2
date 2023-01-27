from pydantic import Field

from src.configs.base import BaseConfig


class RedisConfig(BaseConfig):
    """Настройки Redis."""

    host: str = Field("127.0.0.1", env="REDIS_HOST")
    """Имя хоста."""
    port: int = Field(6379, env="REDIS_PORT")
    """Номер порта."""
    db: int = Field(0, env="REDIS_DB")
    """Номер БД."""
    cache_expires: int = Field(60, env="REDIS_CACHE_EXPIRES")
    """Кол-во секунд хранения кэша."""


redis_config = RedisConfig()
