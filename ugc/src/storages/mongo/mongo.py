from bson import ObjectId
import typing as t
import uuid

from pymongo.errors import DuplicateKeyError

from src.storages.base import Storage, ReviewSort
from src.storages.errors import DuplicateError
from src.storages.mongo.collections.favs import FavsCollection
from src.storages.mongo.collections.reviews import ReviewsCollection
from src.storages.mongo.collections.ratings import RatingsCollection, \
                                                   ObjectType
from src.models.review import Review
from src.models.rating import LikeDislikeRating, MovieRating


class Mongo(Storage):
    """Хранилище Mongo.

    Args:
        favs: коллекция избранных фильмов
        ratings: коллекция оценок
        reviews: коллекция рецензий

    """

    def __init__(
        self,
        favs: FavsCollection,
        ratings: RatingsCollection,
        reviews: ReviewsCollection
    ) -> None:
        self.favs = favs
        self.ratings = ratings
        self.reviews = reviews

    def add_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        try:
            self.ratings.add(
                object_id=movie_id,
                object_type=ObjectType.MOVIE,
                username=username,
                rating=rating
            )
        except DuplicateKeyError:
            raise DuplicateError()

    def edit_rating(
        self,
        movie_id: uuid.UUID,
        username: str,
        rating: int
    ) -> None:
        self.ratings.edit(
            object_id=movie_id,
            object_type=ObjectType.MOVIE,
            username=username,
            rating=rating
        )

    def delete_rating(self, movie_id: uuid.UUID, username: str) -> None:
        self.ratings.delete(
            object_id=movie_id,
            object_type=ObjectType.MOVIE,
            username=username
        )

    def get_rating(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> t.Union[int, None]:
        return self.ratings.get(
            object_id=movie_id,
            object_type=ObjectType.MOVIE,
            username=username
        )

    def get_overall_rating(self, movie_id: uuid.UUID) -> t.Union[float, None]:
        return self.ratings.get_aggregated_rating(
            object_id=movie_id,
            object_type=ObjectType.MOVIE
        )

    def add_to_fav(self, movie_id: uuid.UUID, username: str) -> None:
        self.favs.add(movie_id=movie_id, username=username)

    def delete_from_fav(self, movie_id: uuid.UUID, username: str) -> None:
        self.favs.delete(movie_id=movie_id, username=username)

    def get_favs(self, username: str) -> t.List[uuid.UUID]:
        return self.favs.get(username=username)

    def get_review_movie_rating(
        self,
        movie_id: uuid.UUID,
        username: str
    ) -> MovieRating:
        """"Получить рейтинги фильма для рецензии.

        Args:
            movie_id: ИД фильма
            username: имя пользователя

        Returns:
            MovieRating: модель с оценкой автора и общей

        """
        creator_rating = self.ratings.get(
            object_id=movie_id,
            object_type=ObjectType.MOVIE,
            username=username
        )
        overall_rating = self.ratings.get_aggregated_rating(
            object_id=movie_id,
            object_type=ObjectType.MOVIE
        )
        return MovieRating(
            creator=creator_rating,
            overall=overall_rating
        )

    def add_review(
        self,
        username: str,
        movie_id: uuid.UUID,
        text: str
    ) -> t.Any:
        try:
            review_rating = LikeDislikeRating()
            movie_rating = self.get_review_movie_rating(
                movie_id=movie_id,
                username=username
            )

            return self.reviews.add(
                text=text,
                movie_id=movie_id,
                username=username,
                review_rating=review_rating,
                moview_rating=movie_rating
            )
        except DuplicateKeyError:
            raise DuplicateError()

    def get_reviews(
        self,
        movie_id: uuid.UUID,
        sort: t.Optional[ReviewSort] = None
    ) -> t.List[Review]:
        reviews = self.reviews.get_list(
            movie_id=movie_id,
            sort=sort
        )
        return [Review(**review) for review in reviews]

    def add_review_rating(self, review_id: t.Any, username: str, rating: int):
        try:
            self.ratings.add(
                object_id=ObjectId(review_id),
                object_type=ObjectType.REVIEW,
                username=username,
                rating=rating
            )
        except DuplicateKeyError:
            raise DuplicateError()
