import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation
import enum

import pymongo
from pymongo import collection

from src.storages.base import Storage
from src.configs.mongo import mongo_config
from src.models.fav_movie import FavMovie
from src.models.movie_score import MovieScore


class Collection(str, enum.Enum):
    """Перечисление коллекций."""

    FAV_MOVIES = "fav_movies"
    """Избранные фильмы."""
    MOVIES_SCORE = "movies_score"
    """Оценки фильмов."""


class Mongo(Storage):
    """Хранилище MongoDB."""

    def __init__(self) -> None:
        uri = (
            f'mongodb://{mongo_config.username}:{mongo_config.password}'
            f'@{mongo_config.host}:{mongo_config.port}'
        )
        self.client = pymongo.MongoClient(uri)  # type: pymongo.MongoClient
        self.db = self.client[mongo_config.db]

    def populate(
        self,
        fav_movies: list[FavMovie],
        movies_score: list[MovieScore]
    ):
        self.insert_many(
            collection=Collection.MOVIES_SCORE,
            data=[row.dict() for row in movies_score]
        )
        self.insert_many(
            collection=Collection.FAV_MOVIES,
            data=[row.dict() for row in fav_movies]
        )

    def insert_many(self, collection: Collection, data: list):
        coll = self.get_collection(collection)
        coll.insert_many(data)

    def get_collection(self, collection: Collection) -> collection.Collection:
        """Получить коллецию из MongoDB с настроенным кодеком для работы с UUID.

        Args:
            collection: коллеция из перечисления

        """
        return self.db.get_collection(
            name=collection.value,
            codec_options=CodecOptions(
                uuid_representation=UuidRepresentation.STANDARD
            )
        )

    def add_movie_score(self, movie_score: MovieScore):
        collection = self.get_collection(Collection.MOVIES_SCORE)
        collection.insert_one(movie_score.dict())

    def get_movie_score(self, movie_id: uuid.UUID) -> float | None:
        collection = self.get_collection(Collection.MOVIES_SCORE)
        data = list(collection.aggregate([
            {
                "$match": {
                    "movie_id": movie_id
                }
            },
            {
                "$group": {
                    "_id": "movie_id",
                    "avg_score": {
                        "$avg": "$score"
                    }
                }
            }
        ]))
        if not data:
            return None
        return data[0]["avg_score"]

    def add_fav_movie(self, fav_movie: FavMovie):
        collection = self.get_collection(Collection.FAV_MOVIES)
        collection.insert_one(fav_movie.dict())

    def get_fav_movies(self, user_id: uuid.UUID) -> list[FavMovie]:
        collection = self.get_collection(Collection.FAV_MOVIES)
        data = collection.find({"user_id": user_id})
        return [FavMovie(**row) for row in data]
