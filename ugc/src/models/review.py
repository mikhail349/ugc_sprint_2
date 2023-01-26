from typing import Any, Optional
import datetime
import uuid

from pydantic import BaseModel, Field


class MovieRating(BaseModel):
    """Модель рейтингов фильма."""
    creator: Optional[int] = None
    overall: Optional[float] = None


class ReviewRating(BaseModel):
    """Модель рейтингов рецензии."""
    likes: int
    dislikes: int


class Review(BaseModel):
    """Модель рецензии."""
    id: Any = Field(alias="_id")
    creator: str
    movie_id: uuid.UUID
    text: str
    created_at: datetime.datetime
    movie_rating: MovieRating
    review_rating: ReviewRating
