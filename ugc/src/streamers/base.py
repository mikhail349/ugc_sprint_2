from abc import ABC, abstractmethod


class Streamer(ABC):
    """Абстрактный стример событий."""

    @abstractmethod
    def send_view(self, username: str, movie_id: str, timestamp: int):
        """Отправить событие просмотра.

        Args:
            username: имя пользователя
            movie_id: ИД фильма
            timestamp: кол-во просмотренных секунд
        """

    @abstractmethod
    def send_review_rating(self, username: str, review_id: str, rating: int):
        """Отправить рейтинг рецензии.

        Args:
            username: имя пользователя, который поставлил оценку
            review_id: ИД рецензии
            rating: оценка
        """
