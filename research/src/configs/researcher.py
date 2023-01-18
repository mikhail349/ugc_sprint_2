from pydantic import Field

from src.configs.base import BaseConfig


class ResearcherConfig(BaseConfig):
    """Настройки класса для проведения исследования."""

    user_amount: int = Field(10, env='USER_AMOUNT')
    """Кол-во пользователей."""
    movie_amount: int = Field(10, env='MOVIE_AMOUNT')
    """Кол-во фильмов."""
    read_amount: int = Field(5, env='READ_AMOUNT')
    """Кол-во итераций чтения данных."""


researcher_config = ResearcherConfig()
