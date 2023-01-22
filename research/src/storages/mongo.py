import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation

import pymongo
from pymongo.collection import Collection as MongoCollection

from src.storages.base import Storage
from src.configs.mongo import mongo_config
from src.models.fav_movie import FavMovie
from src.models.movie_score import MovieScore
from src.factories.movie import create_movie
from src.factories.movie_score import create_movie_score


class Mongo(Storage):
    """Хранилище MongoDB."""

    def __init__(self) -> None:
        uri = (
            f'mongodb://{mongo_config.host}:{mongo_config.port}'
        )
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[mongo_config.db]
        self.init_collections()

    def init_collections(self):
        """Инициализировать коллекции."""
        def get_collection(name: str) -> MongoCollection:
            """Получить коллецию MongoDB с настроенным кодеком для работы с UUID.

            Args:
                name: название

            """
            return self.db.get_collection(
                name=name,
                codec_options=CodecOptions(
                    uuid_representation=UuidRepresentation.STANDARD
                )
            )

        self.scores = get_collection("movies_score")
        self.scores.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
                ("user_id", pymongo.ASCENDING)
            ],
            unique=True
        )

        self.movies = get_collection("movies")
        self.movies.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
            ],
            unique=True
        )

        self.favs = get_collection("fav_movies")
        self.favs.create_index(
            [
                ("user_id", pymongo.ASCENDING),
            ],
            unique=True
        )

    def populate(
        self,
        users: list[uuid.UUID],
        fav_movies_per_user: int,
        movies: list[uuid.UUID],
        scores_per_movie: int
    ):
        fav_movies = [
            {
                "user_id": user,
                "fav_movies": [
                    create_movie().id
                    for _ in range(fav_movies_per_user)
                ]
            }
            for user in users
        ]
        self.favs.insert_many(fav_movies)

        movies_score = [
           create_movie_score(movie_id=movie).dict()
           for _ in range(scores_per_movie)
           for movie in movies
        ]
        self.scores.insert_many(movies_score)

    def calculate_movie_score(self, movie_id: uuid.UUID):
        """Рассчитать оценку фильма.

        movie_id: ИД фильма

        """
        scores = list(self.scores.aggregate([
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
        movie_score = scores[0]["avg_score"] if scores else None
        self.movies.update_one(
            {
                "movie_id": movie_id
            },
            {
                "$set": {
                    "score": movie_score
                }
            },
            upsert=True
        )

    def add_movie_score(self, movie_score: MovieScore):
        with self.client.start_session() as session:
            with session.start_transaction():
                self.scores.insert_one(movie_score.dict())
                self.calculate_movie_score(movie_id=movie_score.movie_id)

    def get_movie_score(self, movie_id: uuid.UUID) -> float | None:
        movie = self.movies.find_one({"movie_id": movie_id})
        if not movie:
            return None
        return movie["score"]

    def add_fav_movie(self, fav_movie: FavMovie):
        self.favs.update_one(
            {
                "user_id": fav_movie.user_id
            },
            {
                "$addToSet": {
                    "fav_movies": fav_movie.movie_id
                }
            },
            upsert=True
        )

    def get_fav_movies(self, user_id: uuid.UUID) -> list[uuid.UUID]:
        data = self.favs.find_one({"user_id": user_id})
        if not data:
            return []
        return data["fav_movies"]
