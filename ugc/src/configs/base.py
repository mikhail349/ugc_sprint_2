import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
"""Путь до корня проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    def uppercased_dict(self):
        """Получить параметры настройки в виде словаря с UPPER_CASE ключами"""
        return {k.upper(): v for k, v in self.dict().items()}

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
