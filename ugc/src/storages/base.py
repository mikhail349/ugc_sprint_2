from abc import ABC, abstractmethod
import uuid


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
    ) -> int | None:
        """Получить свою оценку фмльма.

        Args
            movie_id: ИД фильма
            username: имя пользователя

        Returns:
            int | None: оценка или None

        """

    @abstractmethod
    def get_overall_rating(self, movie_id: uuid.UUID) -> float | None:
        """Получить оценку фмльма.

        Args
            movie_id: ИД фильма

        Returns:
            float | None: оценка или None

        """

    @abstractmethod
    def add_to_fav(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> None:
        """Добавить фильм в избранное.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """

    @abstractmethod
    def delete_from_fav(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> None:
        """Удалить фильм из избранного.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """

    @abstractmethod
    def get_favs(
        self,
        username: str
    ) -> list[uuid.UUID]:
        """Получить избранные фильмы.

        Args:
            username: имя пользователя

        """
