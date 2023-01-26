from abc import ABC, abstractmethod
import typing as t
import uuid
import enum

from src.models.review import Review


class ReviewSort(str, enum.Enum):
    """Вид сортировки рецензии."""
    NEWEST = "newest"
    """Сначала новые."""
    OLDEST = "oldest"
    """Сначала старые."""
    MOST_LIKED = "most_liked"
    """Наибольшее кол-во лайков."""
    MOST_DISLIKED = "most_disliked"
    """Наибольшее кол-во дизлайков."""


class Storage(ABC):
    """Абстрактное хранилище."""

    @abstractmethod
    def add_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        """Поставить оценку фильму.

        Args:
            movie_id: ИД фильма
            username: имя пользователя
            rating: рейтинг

        """

    @abstractmethod
    def edit_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        """Изменить оценку фильма.

        Args:
            movie_id: ИД фильма
            username: имя пользователя
            rating: рейтинг

        """

    @abstractmethod
    def delete_rating(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> None:
        """Удалить оценку фмльма.

        Args
            movie_id: ИД фильма
            username: имя пользователя

        """

    @abstractmethod
    def get_rating(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> t.Union[int, None]:
        """Получить свою оценку фмльма.

        Args
            movie_id: ИД фильма
            username: имя пользователя

        Returns:
            int | None: оценка или None

        """

    @abstractmethod
    def get_overall_rating(self, movie_id: uuid.UUID) -> t.Union[float, None]:
        """Получить оценку фмльма.

        Args
            movie_id: ИД фильма

        Returns:
            float | None: оценка или None

        """

    @abstractmethod
    def add_to_fav(self, movie_id: uuid.UUID, username: str) -> None:
        """Добавить фильм в избранное.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """

    @abstractmethod
    def delete_from_fav(self, movie_id: uuid.UUID, username: str) -> None:
        """Удалить фильм из избранного.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """

    @abstractmethod
    def get_favs(self, username: str) -> t.List[uuid.UUID]:
        """Получить избранные фильмы.

        Args:
            username: имя пользователя

        """

    @abstractmethod
    def add_review(
        self,
        username: str,
        movie_id: uuid.UUID,
        text: str
    ) -> t.Any:
        """Добавить рецензию к фильму.

        Args:
            username: имя пользователя
            movie_id: ИД фильма
            text: текст рецензии

        Returns:
            Any: ИД рецензии

        """

    @abstractmethod
    def get_reviews(
        self,
        movie_id: uuid.UUID,
        sort: t.Optional[ReviewSort] = None
    ) -> t.List[Review]:
        """Получить список рецензий к фильму.

        Args:
            movie_id: ИД фильма
            sort: сортировка

        Returns:
            list[Review]: список рецензий

        """

    @abstractmethod
    def add_review_rating(self, review_id: t.Any, username: str, rating: int):
        """Поставить оценку ревью.

        Args:
            review_id: ИД рецензии
            username: имя пользователя
            rating: оценка

        """
