import uuid

import clickhouse_driver

from src.storages.base import Storage
from src.models.fav_movie import FavMovie
from src.models.movie_score import MovieScore
from src.configs.clickhouse import clickhouse_config
from src.factories.movie_score import create_movie_score
from src.factories.fav_movie import create_fav_movie


class Clickhouse(Storage):
    """Класс хранилища Clickhouse."""

    def populate(
        self,
        users: list[uuid.UUID],
        fav_movies_per_user: int,
        movies: list[uuid.UUID],
        scores_per_movie: int
    ):
        client = get_client()

        sql = (
            f"INSERT INTO "
            f"{clickhouse_config.db_name}.movies_score "
            f"(id, user_id, movie_id, score) VALUES"
        )

        movies_score = [
           create_movie_score(movie_id=movie)
           for _ in range(scores_per_movie)
           for movie in movies
        ]

        client.execute(
            sql,
            [
                (
                    str(movie_score.id),
                    str(movie_score.user_id),
                    str(movie_score.movie_id),
                    movie_score.score
                )
                for movie_score in movies_score
            ]
        )

        sql = (
            f"INSERT INTO "
            f"{clickhouse_config.db_name}.fav_movies "
            f"(id, user_id, movie_id) VALUES"
        )

        fav_movies = [
           create_fav_movie(user_id=user)
           for _ in range(fav_movies_per_user)
           for user in users
        ]

        client.execute(
            sql,
            [
                (
                    str(fav_movie.id),
                    str(fav_movie.user_id),
                    str(fav_movie.movie_id),
                )
                for fav_movie in fav_movies
            ]
        )

    def add_movie_score(self, movie_score: MovieScore):
        sql = (
            f"INSERT INTO "
            f"{clickhouse_config.db_name}.movies_score "
            f"(id, user_id, movie_id, score) VALUES"
        )
        batch = [
            (
                str(movie_score.id),
                str(movie_score.user_id),
                str(movie_score.movie_id),
                movie_score.score
            ),
        ]
        get_client().execute(sql, batch)

    def add_fav_movie(self, fav_movie: FavMovie):
        sql = (
            f"INSERT INTO "
            f"{clickhouse_config.db_name}.fav_movies "
            f"(id, user_id, movie_id) VALUES"
        )
        batch = (
            (
                str(fav_movie.id),
                str(fav_movie.user_id),
                str(fav_movie.movie_id),
            ),
        )
        get_client().execute(sql, batch)

    def get_movie_score(self, movie_id: uuid.UUID) -> float | None:
        sql = (
            f"SELECT avg(score) as avg_score FROM "
            f"{clickhouse_config.db_name}.movies_score "
            f"WHERE movie_id = '{movie_id}'"
        )
        data = get_client().query_dataframe(sql).to_dict("records")
        if not data:
            return None
        return data[0]["avg_score"]

    def get_fav_movies(self, user_id: uuid.UUID) -> list[uuid.UUID]:
        sql = (
            f"SELECT movie_id FROM "
            f"{clickhouse_config.db_name}.fav_movies "
            f"WHERE user_id = '{user_id}'"
        )
        data = get_client().query_dataframe(sql).to_dict("records")
        return [row["movie_id"] for row in data]


def get_client() -> clickhouse_driver.Client:
    """Получить инстанс клиента Clickhouse."""
    return clickhouse_driver.Client(host=clickhouse_config.host)
