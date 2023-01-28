import enum
from typing import Any, Union

from pymongo.database import Database as MongoDatabase
import pymongo

from src.storages.mongo.collections.base import BaseCollection
from src.storages.errors import DoesNotExistError
from src.models.rating import LikeDislikeRating


class ObjectType(str, enum.Enum):
    """Вид объекта, для которого ставится оценка."""
    MOVIE = "movie"
    """Фильм."""
    REVIEW = "review"
    """Рецензия."""


class RatingsCollection(BaseCollection):
    """Класс коллекции оценок."""

    def __init__(self, db: MongoDatabase) -> None:
        super().__init__(db)

        self.coll = self.get_collection("ratings")
        self.coll.create_index(
            [
                ("object_id", pymongo.ASCENDING),
                ("object_type", pymongo.ASCENDING),
                ("username", pymongo.ASCENDING)
            ],
            unique=True
        )

    def add(
        self,
        object_id: Any,
        object_type: ObjectType,
        username: str,
        rating: int
    ):
        """Поставить оценку.

        Args:
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`
            username: имя пользователя
            rating: рейтинг

        """
        self.coll.insert_one({
            "object_id": object_id,
            "object_type": object_type.value,
            "username": username,
            "rating": rating
        })

    def edit(
        self,
        object_id: Any,
        object_type: ObjectType,
        username: str,
        rating: int
    ) -> None:
        """Изменить оценку.

        Args:
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`
            username: имя пользователя
            rating: рейтинг

        """
        result = self.coll.find_one_and_update(
            {
                "object_id": object_id,
                "object_type": object_type.value,
                "username": username
            },
            {
                "$set": {
                    "rating": rating
                }
            }
        )
        if not result:
            raise DoesNotExistError()

    def delete(
        self,
        object_id: Any,
        object_type: ObjectType,
        username: str
    ):
        """Удалить оценку.

        Args
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`
            username: имя пользователя

        """
        result = self.coll.find_one_and_delete({
            "object_id": object_id,
            "object_type": object_type.value,
            "username": username
        })
        if not result:
            raise DoesNotExistError()

    def get(
        self,
        object_id: Any,
        object_type: ObjectType,
        username: str
    ) -> Union[int, None]:
        """Получить оценку пользователя.

        Args
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`
            username: имя пользователя

        Returns:
            int | None: оценка или None

        """
        result = self.coll.find_one({
            "object_id": object_id,
            "object_type": object_type.value,
            "username": username
        })
        if result:
            return result["rating"]
        return None

    def get_aggregated_rating(
        self,
        object_id: Any,
        object_type: ObjectType
    ) -> Union[float, None]:
        """Получить агрегированную оценку.

        Args
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`

        Returns:
            float | None: оценка или None

        """
        ratings = list(self.coll.aggregate([
            {
                "$match": {
                    "object_id": object_id,
                    "object_type": object_type.value
                }
            },
            {
                "$group": {
                    "_id": "movie_id",
                    "avg_rating": {
                        "$avg": "$rating"
                    }
                }
            }
        ]))
        if ratings:
            return ratings[0]["avg_rating"]
        return None

    def get_likes_dislikes_count(
        self,
        object_id: Any,
        object_type: ObjectType
    ) -> LikeDislikeRating:
        """Получить количество лайков и дизлайков.

        Args
            object_id: ИД объекта
            object_type: тип объекта класса `ObjectType`

        Returns:
            `LikeDislikeRating`: модель с количеством лайков и дизлайков

        """
        result = list(self.coll.aggregate([
            {
                "$match": {
                    "object_id": object_id,
                    "object_type": object_type.value,
                }
            },
            {
                "$project": {
                    "likes": {"$cond": [{"$eq": ["$rating", 10]}, 1, 0]},
                    "dislikes": {"$cond": [{"$eq": ["$rating", 0]}, 1, 0]},
                }
            },
            {
                "$group": {
                    "_id": "object_id",
                    "likes": {
                        "$sum": "$likes"
                    },
                    "dislikes": {
                        "$sum": "$dislikes"
                    }
                }
            }
        ]))

        return LikeDislikeRating(
            likes=result[0]["likes"] if result else 0,
            dislikes=result[0]["dislikes"] if result else 0
        )
