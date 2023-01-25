import typing as t
import uuid
from bson import ObjectId
import datetime

from pymongo.database import Database as MongoDatabase
import pymongo

from src.storages.base import ReviewSort
from src.storages.mongo.collections.base import BaseCollection
from src.models.rating import LikeDislikeRating, MovieRating


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


class ReviewsCollection(BaseCollection):
    """Класс коллекции рецензий."""

    def __init__(self, db: MongoDatabase) -> None:
        super().__init__(db)

        self.coll = self.get_collection("reviews")
        self.coll.create_index(
            [
                ("movie_id", pymongo.ASCENDING),
                ("creator", pymongo.ASCENDING)
            ],
            unique=True
        )

    def add(
        self,
        text: str,
        movie_id: uuid.UUID,
        username: str,
        moview_rating: MovieRating,
        review_rating: LikeDislikeRating
    ) -> ObjectId:
        """Добавить рецензию.

        Args:
            text: текст рецензии
            movie_id: ИД фильма
            username: имя пользователя-автора
            moview_rating: оценка фильма `MovieRating`
            review_rating: оценка рецензии `LikeDislikeRating`

        Returns:
            ObjectId: ИД рецензии

        """
        result = self.coll.insert_one({
            "creator": username,
            "movie_id": movie_id,
            "text": text,
            "created_at": datetime.datetime.now(),
            "movie_rating": moview_rating.dict(),
            "review_rating": review_rating.dict()
        })
        return result.inserted_id

    def update(
        self,
        review_id: t.Any,
        review_rating: LikeDislikeRating,
        moview_rating: MovieRating
    ):
        """Обновить данные рецензии.

        Args:
            review_id: ИД рецензии
            review_rating: оценка рецензии `LikeDislikeRating`
            moview_rating: оценка фильма `MovieRating`
        """
        self.coll.update_one(
            {
                "_id": review_id
            },
            {
                "$set": {
                    "movie_rating": moview_rating.dict(),
                    "review_rating": review_rating.dict()
                }
            }
        )

    def get(self, filter: dict[str, str]) -> dict | None:
        """Получить данные рецензии.

        Args:
            filter: словарь поиска рецензии

        Returns:
            dict | None: словарь с данными рецензии или None

        """
        return self.coll.find_one(filter)

    def get_list(
        self,
        movie_id: uuid.UUID,
        sort: ReviewSort = None
    ) -> list:
        """Получить отсортированный список рецензий фильма.

        Args:
            movie_id: ИД фильма
            sort: сортировка `ReviewSort`

        Returns:
            list: список рецензий

        """
        pipeline = [
            {
                "$match": {
                    "movie_id": movie_id
                }
            }
        ]
        if sort:
            pipeline.append(get_review_sort_query(sort))

        return list(self.coll.aggregate(pipeline))
