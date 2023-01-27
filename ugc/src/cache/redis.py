import typing as t

import redis

from src.cache.base import Cache


class Redis(Cache):
    """Кэш Redis.

    Args:
        redis: соединение с Redis
        cache_expires: кол-во секунд хранения кэша

    """

    def __init__(self, redis: redis.Redis, cache_expires: int) -> None:
        self.redis = redis
        self.cache_expires = cache_expires

    def get(self, key: str) -> t.Optional[t.Any]:
        return self.redis.get(key)

    def put(self, key: str, value: t.Any):
        self.redis.set(key, value, ex=self.cache_expires)
