from abc import ABC, abstractmethod
import uuid

from src.models.fav_movie import FavMovie
from src.models.movie_score import MovieScore


class Storage(ABC):
    """Абстрактное хранилище."""

    @abstractmethod
    def populate(
        self,
        fav_movies: list[FavMovie],
        movies_score: list[MovieScore]
    ):
        """Наполнить хранилище."""

    @abstractmethod
    def add_movie_score(self, movie_score: MovieScore):
        """Поставить оценку фильму.

        Args:
            movie_score: инстанс MovieScore
        """

    @abstractmethod
    def get_movie_score(self, movie_id: uuid.UUID) -> float | None:
        """Получить среднюю оценку фильма.

        Args:
            movie_id: ИД фильма.
        """

    @abstractmethod
    def add_fav_movie(self, fav_movie: FavMovie):
        """Добавить фильм в избранное.

        Args:
            fav_movie: инстанс FavMovie
        """

    @abstractmethod
    def get_fav_movies(self, user_id: uuid.UUID) -> list[FavMovie]:
        """Получить список избранных фильмов пользователя.

        Args:
            user_id: ИД записи пользователя
        """
