import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation
import datetime

import pymongo
from pymongo.collection import Collection as MongoCollection
from pymongo.errors import DuplicateKeyError

from src.storages.base import Storage
from src.configs.mongo import mongo_config
from src.storages.errors import DuplicateError, DoesNotExistError


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
                ("movie_id", pymongo.ASCENDING),
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
                ("username", pymongo.ASCENDING)
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
                    "movie_id": movie_id
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
                        "movie_id": movie_id,
                        "username": username,
                        "rating": rating
                    })
                    self.update_movie(movie_id=movie_id)
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
                        "movie_id": movie_id,
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

    def delete_rating(self, movie_id: uuid.UUID, username: str) -> None:
        with self.client.start_session() as session:
            with session.start_transaction():
                result = self.ratings.find_one_and_delete(
                    {
                        "movie_id": movie_id,
                        "username": username
                    }
                )
                print(result)
                if not result:
                    raise DoesNotExistError()
                self.update_movie(movie_id=movie_id)

    def get_rating(self, movie_id: uuid.UUID, username: str) -> int | None:
        result = self.ratings.find_one({
            "movie_id": movie_id,
            "username": username
        })
        if not result:
            raise DoesNotExistError()

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

    def add_review(self, username: str, movie_id: uuid.UUID, text: str):
        try:
            self.reviews.insert_one({
                "username": username,
                "movie_id": movie_id,
                "text": text,
                "created_at": datetime.datetime.now()
            })
        except DuplicateKeyError:
            raise DuplicateError()

    def get_reviews(self, movie_id: uuid.UUID) -> list:
        reviews = list(self.reviews.aggregate([
            {
                "$match": {
                    "movie_id": movie_id
                }
            },
            {
                "$lookup": {
                    "from": "ratings",
                    "let": {
                        "movie_id": "$movie_id",
                        "username": "$username"
                    },
                    "pipeline": [{
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {
                                        "$eq": [
                                            "$movie_id",
                                            "$$movie_id"
                                        ]
                                    },
                                    {
                                        "$eq": [
                                            "$username",
                                            "$$username"
                                        ]
                                    }
                                ]
                            }
                        }
                    }],
                    "as": "movie_ratings"
                }
            }
        ]))
        if not reviews:
            return []

        return [{
            "created_at": review["created_at"],
            "creator": {
                "username": review["username"]
            },
            "movie_rating": (
                review["movie_ratings"][0]["rating"]
                if review["movie_ratings"] else None
            ),
            "text": review["text"]
        } for review in reviews]
