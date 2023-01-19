from abc import ABC, abstractmethod


class Storage(ABC):
    """Абстрактное хранилище событий."""

    @abstractmethod
    def create_view_event(
        self,
        username: str,
        movie_id: str,
        timestamp: int
    ) -> None:
        """Добавить событие просмотра.

        Args:
            username: имя пользователя
            movie_id: ИД фильма
            timestamp: кол-во просмотренных секунд
        """
