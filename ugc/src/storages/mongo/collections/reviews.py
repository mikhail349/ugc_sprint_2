import typing as t
import uuid
from bson import ObjectId
import datetime

from pymongo.database import Database as MongoDatabase
import pymongo

from src.storages.base import ReviewSort
from src.storages.mongo.collections.base import BaseCollection
from src.storages.mongo.collections.ratings import ObjectType


def get_review_sort_query(sort: ReviewSort) -> t.Dict:
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
        username: str
    ) -> ObjectId:
        """Добавить рецензию.

        Args:
            text: текст рецензии
            movie_id: ИД фильма
            username: имя пользователя-автора

        Returns:
            ObjectId: ИД рецензии

        """
        result = self.coll.insert_one({
            "creator": username,
            "movie_id": movie_id,
            "text": text,
            "created_at": datetime.datetime.now()
        })
        return result.inserted_id

    def get(self, filter: t.Dict[str, str]) -> t.Union[t.Dict, None]:
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
        sort: t.Optional[ReviewSort] = None
    ) -> list:
        """Получить отсортированный список рецензий фильма.

        Args:
            movie_id: ИД фильма
            sort: сортировка `ReviewSort`

        Returns:
            list: список рецензий

        """
        OBJ_MOVIE = ObjectType.MOVIE.value
        pipeline = [
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
                        "creator": "$creator"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$object_id",  "$$movie_id"]},
                                        {"$eq": ["$object_type", OBJ_MOVIE]}
                                    ]
                                }
                            }
                        },
                        {
                            "$project": {
                                "creator_rating": {
                                    "$cond": [
                                        {
                                            "$eq": [
                                                "$username", "$$creator"
                                            ]
                                        },
                                        "$rating", 0
                                    ]
                                },
                                "rating": "$rating"
                            }
                        },
                        {
                            "$group": {
                                "_id": "$object_id",
                                "creator": {
                                    "$sum": "$creator_rating",
                                },
                                "overall": {
                                    "$avg": "$rating",
                                }
                            }
                        },
                    ],
                    "as": "movie_rating"
                }
            },
            {
                "$lookup": {
                    "from": "ratings",
                    "let": {
                        "review_id": "$_id"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$object_id",  "$$review_id"]
                                }
                            }
                        },
                        {
                            "$project": {
                                "likes": {
                                    "$cond": [
                                        {"$eq": ["$rating", 10]}, 1, 0
                                    ]
                                },
                                "dislikes": {
                                    "$cond": [
                                        {"$eq": ["$rating", 0]}, 1, 0
                                    ]
                                },
                            }
                        },
                        {
                            "$group": {
                                "_id": "$object_id",
                                "likes": {
                                    "$sum": "$likes"
                                },
                                "dislikes": {
                                    "$sum": "$dislikes"
                                }
                            }
                        }
                    ],
                    "as": "review_rating"
                }
            },
            {
                "$unwind": {
                    "path": "$movie_rating",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$unwind": {
                    "path": "$review_rating",
                    "preserveNullAndEmptyArrays": True
                }
            },
        ]
        if sort:
            pipeline.append(get_review_sort_query(sort))

        return list(self.coll.aggregate(pipeline))
