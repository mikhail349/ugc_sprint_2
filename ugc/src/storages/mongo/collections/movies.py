import uuid
import typing as t

from pymongo.database import Database as MongoDatabase
import pymongo

from src.storages.mongo.collections.base import BaseCollection


class MoviesCollection(BaseCollection):
    """Класс коллекции фильмов."""

    def __init__(self, db: MongoDatabase) -> None:
        super().__init__(db)

        self.coll = self.get_collection("movies")
        self.coll.create_index(
            [
                ("username", pymongo.ASCENDING),
            ],
            unique=True
        )

    def get(self, movie_id: uuid.UUID) -> t.Union[t.Dict, None]:
        """Получить данные фильма.

        Args:
            movie_id: ИД фильма

        Returns:
            dict | None: словарь с данными фильма или None

        """
        return self.coll.find_one({"movie_id": movie_id})

    def update(self, movie_id: uuid.UUID, rating: t.Optional[float]):
        """Обновить фильм.

        Args:
            movie_id: ИД фильма
            rating: рейтинг фильма

        """
        self.coll.update_one(
            {
                "movie_id": movie_id
            },
            {
                "$set": {
                    "rating": rating
                }
            },
            upsert=True
        )
