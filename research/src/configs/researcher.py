from pydantic import Field

from src.configs.base import BaseConfig


class ResearcherConfig(BaseConfig):
    """Настройки класса для проведения исследования."""

    user_amount: int = Field(10, env="USER_AMOUNT")
    """Кол-во пользователей."""
    fav_movies_per_user_amount: int = Field(50,
                                            env="FAV_MOVIES_PER_USER_AMOUNT")
    """Кол-во избранных фильмов у одного пользователя."""
    movie_amount: int = Field(10, env="MOVIE_AMOUNT")
    """Кол-во фильмов."""
    scores_per_movie_amount: int = Field(100,
                                         env="SCORES_PER_MOVIE_AMOUNT")
    read_amount: int = Field(5, env="READ_AMOUNT")
    """Кол-во итераций чтения данных."""


researcher_config = ResearcherConfig()
