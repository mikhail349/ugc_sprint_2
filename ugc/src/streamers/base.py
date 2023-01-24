from abc import ABC, abstractmethod


class Streamer(ABC):
    """Абстрактный стример событий."""

    @abstractmethod
    def send_view(
        self,
        username: str,
        movie_id: str,
        timestamp: int
    ) -> None:
        """Отправить событие просмотра.

        Args:
            username: имя пользователя
            movie_id: ИД фильма
            timestamp: кол-во просмотренных секунд
        """
