import typing as t
import datetime
import uuid

from pydantic import BaseModel, Field

from src.models.rating import MovieRating, LikeDislikeRating


class Review(BaseModel):
    """Модель рецензии."""
    id: t.Any = Field(alias="_id")
    creator: str
    movie_id: uuid.UUID
    text: str
    created_at: datetime.datetime
    movie_rating: t.Optional[MovieRating] = None
    review_rating: t.Optional[LikeDislikeRating] = None
