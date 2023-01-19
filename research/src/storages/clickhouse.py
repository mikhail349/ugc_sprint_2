import uuid

import clickhouse_driver

from src.storages.base import Storage
from src.models.fav_movie import FavMovie
from src.models.movie_score import MovieScore
from src.configs.clickhouse import clickhouse_config


class Clickhouse(Storage):
    """Класс хранилища Clickhouse."""

    def __init__(self):
        client = get_client()

        client.execute(
            f"CREATE DATABASE IF NOT EXISTS {clickhouse_config.db_name} "
            f"ON CLUSTER {clickhouse_config.cluster_name}"
        )
        client.execute(
            f"CREATE TABLE IF NOT EXISTS "
            f"{clickhouse_config.db_name}.fav_movies "
            f"ON CLUSTER {clickhouse_config.cluster_name} "
            f"(id String, user_id String, movie_id String) "
            f"Engine=MergeTree() ORDER BY id"
        )
        client.execute(
            f"CREATE TABLE IF NOT EXISTS "
            f"{clickhouse_config.db_name}.movies_score "
            f"ON CLUSTER {clickhouse_config.cluster_name} "
            f"(id String, user_id String, movie_id String, score UInt8) "
            f"Engine=MergeTree() ORDER BY id"
        )

    def populate(
        self,
        fav_movies: list[FavMovie],
        movies_score: list[MovieScore]
    ):
        client = get_client()

        sql = (
            f"INSERT INTO "
            f"{clickhouse_config.db_name}.movies_score "
            f"(id, user_id, movie_id, score) VALUES"
        )
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

    def get_fav_movies(self, user_id: uuid.UUID) -> list[FavMovie]:
        sql = (
            f"SELECT * FROM "
            f"{clickhouse_config.db_name}.fav_movies "
            f"WHERE user_id = '{user_id}'"
        )
        data = get_client().query_dataframe(sql).to_dict("records")
        return [FavMovie(**row) for row in data]


def get_client() -> clickhouse_driver.Client:
    """Получить инстанс клиента Clickhouse."""
    return clickhouse_driver.Client(host=clickhouse_config.host)
