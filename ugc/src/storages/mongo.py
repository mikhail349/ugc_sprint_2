import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation

import pymongo

from src.storages.base import Storage
from src.configs.mongo import mongo_config
from src.storages.errors import DuplicateError


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
        self.ratings = self.db.get_collection(
            name="ratings",
            codec_options=CodecOptions(
                uuid_representation=UuidRepresentation.STANDARD
            ))

        self.ratings.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
                ("username", pymongo.ASCENDING)
            ],
            unique=True
        )

    def add_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        try:
            self.ratings.insert_one({
                "movie_id": movie_id,
                "username": username,
                "rating": rating
            })
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateError()

    def edit_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        self.ratings.update_one(
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

    def delete_rating(self, movie_id: uuid.UUID, username: str) -> None:
        self.ratings.delete_one(
            {
                "movie_id": movie_id,
                "username": username
            }
        )

    def get_rating(self, movie_id: uuid.UUID, username: str) -> int | None:
        result = self.ratings.find_one({
            "movie_id": movie_id,
            "username": username
        })
        if result:
            return result["rating"]

    def get_overall_rating(self, movie_id: uuid.UUID) -> float | None:
        result = list(self.ratings.aggregate([
            {
                "$match": {
                    "movie_id": movie_id
                }
            },
            {
                "$group": {
                    "_id": "movie_id",
                    "rating": {
                        "$avg": "$rating"
                    }
                }
            }
        ]))
        if result:
            return result[0]["rating"]
