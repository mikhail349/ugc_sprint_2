"""
Модуль модели оценки фильма.
"""

import uuid

from pydantic import BaseModel, Field


class MovieScore(BaseModel):
    """Класс оценки фильма."""
    id: uuid.UUID
    user_id: uuid.UUID
    movie_id: uuid.UUID
    score: int = Field(ge=0, le=10)
