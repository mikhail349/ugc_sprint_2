from pydantic import Field

from src.configs.base import BaseConfig


class MongoConfig(BaseConfig):
    """Настройки MongoDB."""

    host: str = Field("127.0.0.1", env="MONGODB_HOST")
    """Имя хоста."""
    port: int = Field(27017, env="MONGODB_PORT")
    """Номер порта."""
    db: str = Field("movies", env="MONGODB_DATABASE")
    """Название БД."""
    username: str = Field("root", env="MONGODB_USERNAME")
    """Имя пользователя."""
    password: str = Field("example", env="MONGODB_PASSWORD")
    """Пароль."""


mongo_config = MongoConfig()
