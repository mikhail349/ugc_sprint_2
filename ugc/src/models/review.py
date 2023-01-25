from typing import Any
import datetime
import uuid

from pydantic import BaseModel, Field

from src.models.rating import MovieRating, LikeDislikeRating


class Review(BaseModel):
    """Модель рецензии."""
    id: Any = Field(alias="_id")
    creator: str
    movie_id: uuid.UUID
    text: str
    created_at: datetime.datetime
    movie_rating: MovieRating
    review_rating: LikeDislikeRating
