import uuid
from typing import List

from pymongo.database import Database as MongoDatabase
import pymongo

from src.storages.mongo.collections.base import BaseCollection


class FavsCollection(BaseCollection):
    """Класс коллекции избранных фильмов."""

    def __init__(self, db: MongoDatabase) -> None:
        super().__init__(db)

        self.coll = self.get_collection("favs")
        self.coll.create_index(
            [
                ("username", pymongo.ASCENDING),
            ],
            unique=True
        )

    def add(self, movie_id: uuid.UUID, username: str):
        """Добавить фильм в избранное.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """
        self.coll.update_one(
            {
                "username": username
            },
            {
                "$addToSet": {
                    "fav_movies": movie_id
                }
            },
            upsert=True
        )

    def delete(self, movie_id: uuid.UUID, username: str) -> None:
        """Удалить фильм из избранного.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """
        self.coll.update_one(
            {
                "username": username
            },
            {
                "$pull": {
                    "fav_movies": movie_id
                }
            }
        )

    def get(self, username: str) -> List[uuid.UUID]:
        """Получить избранные фильмы.

        Args:
            username: имя пользователя

        """
        result = self.coll.find_one({"username": username})
        if not result:
            return []
        return result["fav_movies"]
