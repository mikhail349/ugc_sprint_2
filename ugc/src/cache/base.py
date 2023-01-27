from abc import ABC, abstractmethod
import typing as t


class Cache(ABC):
    """Абстрактный класс хранилища кеша."""

    @abstractmethod
    def get(self, key: str) -> t.Optional[t.Any]:
        """Получить данные по ключу из кэша.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные

        """

    @abstractmethod
    def put(self, key: str, value: t.Any):
        """Записать данные в кэш.

        Args:
            key: ключ
            value: данные

        """
