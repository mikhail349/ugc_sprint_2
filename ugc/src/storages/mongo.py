import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation
from bson import ObjectId
import datetime
from typing import Any
import enum

import pymongo
from pymongo.collection import Collection as MongoCollection
from pymongo.errors import DuplicateKeyError

from src.storages.base import Storage, ReviewSort
from src.configs.mongo import mongo_config
from src.storages.errors import DuplicateError, DoesNotExistError
from src.models.review import Review


class RatingObject(str, enum.Enum):
    """Вид объекта, для которого ставится оценка."""
    MOVIE = "movie"
    """Фильм."""
    REVIEW = "review"
    """Рецензия."""


def get_review_sort_query(sort: ReviewSort) -> dict:
    """Получить mongo-запрос для сортировки рецензий.

    Args:
        sort: ReviewSort

    """
    sorts = {
        ReviewSort.NEWEST: {"created_at": -1},
        ReviewSort.OLDEST: {"created_at": 1},
        ReviewSort.MOST_LIKED: {"review_rating.likes": -1},
        ReviewSort.MOST_DISLIKED: {"review_rating.dislikes": -1}
    }
    return {"$sort": sorts.get(sort)}


class Mongo(Storage):
    """Хранилище Mongo."""

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            f"mongodb://{mongo_config.host}:{mongo_config.port}"
        )
        self.db = self.client[mongo_config.db]
        self.init_collections()

    def init_collections(self):
        """Инициализировать коллекции."""
        def get_collection(name: str) -> MongoCollection:
            """Получить коллекцию MongoDB с кодеком UUID.

            Args:
                name: название коллекции

            Returns:
                MongoCollection: коллекция pymongo

            """
            return self.db.get_collection(
                name=name,
                codec_options=CodecOptions(
                    uuid_representation=UuidRepresentation.STANDARD
                )
            )

        self.movies = get_collection("movies")
        self.movies.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
            ],
            unique=True
        )

        self.ratings = get_collection("ratings")
        self.ratings.create_index(
            [
                ("object_id", pymongo.ASCENDING),
                ("object_type", pymongo.ASCENDING),
                ("username", pymongo.ASCENDING)
            ],
            unique=True
        )

        self.favs = get_collection("favs")
        self.favs.create_index(
            [
                ("username", pymongo.ASCENDING),
            ],
            unique=True
        )

        self.reviews = get_collection("reviews")
        self.reviews.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
                ("creator", pymongo.ASCENDING)
            ],
            unique=True
        )

    def update_movie(self, movie_id: uuid.UUID):
        """Обновить данные фильма.

        Args:
            movie_id: ИД фильма

        """
        ratings = list(self.ratings.aggregate([
            {
                "$match": {
                    "object_id": movie_id,
                    "object_type": RatingObject.MOVIE.value
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

        rating = ratings[0]["avg_rating"] if ratings else None
        self.movies.update_one(
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

    def add_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        try:
            with self.client.start_session() as session:
                with session.start_transaction():
                    self.ratings.insert_one({
                        "object_id": movie_id,
                        "object_type": RatingObject.MOVIE.value,
                        "username": username,
                        "rating": rating
                    })
                    self.update_movie(movie_id=movie_id)
                    self.update_review({
                        "movie_id": movie_id,
                        "creator": username
                    })
        except DuplicateKeyError:
            raise DuplicateError()

    def edit_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        with self.client.start_session() as session:
            with session.start_transaction():
                result = self.ratings.find_one_and_update(
                    {
                        "object_id": movie_id,
                        "object_type": RatingObject.MOVIE.value,
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
                self.update_movie(movie_id=movie_id)
                self.update_review({
                    "movie_id": movie_id,
                    "creator": username
                })

    def delete_rating(self, movie_id: uuid.UUID, username: str) -> None:
        with self.client.start_session() as session:
            with session.start_transaction():
                result = self.ratings.find_one_and_delete({
                    "object_id": movie_id,
                    "object_type": RatingObject.MOVIE.value,
                    "username": username
                })
                if not result:
                    raise DoesNotExistError()
                self.update_movie(movie_id=movie_id)
                self.update_review({
                    "movie_id": movie_id,
                    "creator": username
                })

    def get_rating(self, movie_id: uuid.UUID, username: str) -> int | None:
        result = self.ratings.find_one({
            "object_id": movie_id,
            "object_type": RatingObject.MOVIE.value,
            "username": username
        })
        if not result:
            return None
        return result["rating"]

    def get_overall_rating(self, movie_id: uuid.UUID) -> float | None:
        movie = self.movies.find_one({"movie_id": movie_id})
        if not movie:
            return None
        return movie["rating"]

    def add_to_fav(self, movie_id: uuid.UUID, username: str) -> None:
        self.favs.update_one(
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

    def delete_from_fav(self, movie_id: uuid.UUID, username: str) -> None:
        self.favs.update_one(
            {
                "username": username
            },
            {
                "$pull": {
                    "fav_movies": movie_id
                }
            }
        )

    def get_favs(self, username: str) -> list[uuid.UUID]:
        result = self.favs.find_one({"username": username})
        if not result:
            return []
        return result["fav_movies"]

    def get_review_movie_rating(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> dict:
        """"Получить рейтинг фильма в рецензии.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        """
        creator_rating = self.get_rating(
            movie_id=movie_id,
            username=username
        )
        overall_rating = self.get_overall_rating(
            movie_id=movie_id
        )
        return {
            "creator": creator_rating,
            "overall": overall_rating
        }

    def get_review_rating(self, review_id: Any) -> dict:
        """"Получить рейтинг рецензии.

        Args:
            review: ИД рецензии

        """
        result = list(self.ratings.aggregate([
            {
                "$match": {
                    "object_id": review_id,
                    "object_type": RatingObject.REVIEW.value,
                }
            },
            {
                "$project": {
                    "likes": {"$cond": [{"$eq": ['$rating', 10]}, 1, 0]},
                    "dislikes": {"$cond": [{"$eq": ['$rating', 0]}, 1, 0]},
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

        return {
            "likes": result[0]["likes"] if result else 0,
            "dislikes": result[0]["dislikes"] if result else 0
        }

    def update_review(self, filter: dict[str, str]):
        """Обновить рецензию.

        Args:
            filter: словарь поиска рецензии

        """
        review = self.reviews.find_one(filter)
        if not review:
            return

        self.reviews.find_one_and_update(
            {
                "_id": review["_id"]
            },
            {
                "$set": {
                    "movie_rating": self.get_review_movie_rating(
                        movie_id=review["movie_id"],
                        username=review["creator"]
                    ),
                    "review_rating": self.get_review_rating(
                        review_id=review["_id"]
                    )
                }
            }
        )

    def add_review(self, username: str, movie_id: uuid.UUID, text: str) -> Any:
        with self.client.start_session() as session:
            with session.start_transaction():
                try:
                    result = self.reviews.insert_one({
                        "creator": username,
                        "movie_id": movie_id,
                        "text": text,
                        "created_at": datetime.datetime.now(),
                        "movie_rating": self.get_review_movie_rating(
                            movie_id=movie_id,
                            username=username
                        ),
                        "review_rating": {
                            "likes": 0,
                            "dislikes": 0,
                        }
                    })
                    return result.inserted_id
                except DuplicateKeyError:
                    raise DuplicateError()

    def get_reviews(
        self,
        movie_id: uuid.UUID,
        sort: ReviewSort = None
    ) -> list:
        pipeline = [
            {
                "$match": {
                    "movie_id": movie_id
                }
            }
        ]
        if sort:
            pipeline.append(get_review_sort_query(sort))

        reviews = list(self.reviews.aggregate(pipeline))
        return [Review(**review).dict() for review in reviews]

    def add_review_rating(self, review_id: Any, username: str, rating: int):
        with self.client.start_session() as session:
            with session.start_transaction():
                try:
                    self.ratings.insert_one({
                        "object_id": ObjectId(review_id),
                        "object_type": RatingObject.REVIEW.value,
                        "username": username,
                        "rating": rating
                    })
                    self.update_review({
                        "_id": ObjectId(review_id)
                    })
                except DuplicateKeyError:
                    raise DuplicateError()
