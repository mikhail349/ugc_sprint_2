from pydantic import Field

from src.configs.base import BaseConfig


class LoggerConfig(BaseConfig):
    """Настройки логирования."""

    file: str = Field("logs/app.log", env="LOG_FILE")
    """Имя файла для записи логов."""
    file_max_bytes: int = Field(1000, env="LOG_FILE_MAX_BYTES")
    """Максимальный размер файла для записи логов."""


logger_config = LoggerConfig()
