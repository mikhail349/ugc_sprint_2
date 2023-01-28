from abc import ABC, abstractmethod
from typing import Optional, Any


class Cache(ABC):
    """Абстрактный класс хранилища кеша."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Получить данные по ключу из кэша.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные

        """

    @abstractmethod
    def put(self, key: str, value: Any):
        """Записать данные в кэш.

        Args:
            key: ключ
            value: данные

        """
