import os

from pydantic import BaseSettings


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
"""Путь до корня проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс с настройками."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
