import uuid

from pydantic import BaseModel, Field


class MovieRating(BaseModel):
    movie_id: uuid.UUID
    username: str
    rating: int = Field(ge=0, le=10)
