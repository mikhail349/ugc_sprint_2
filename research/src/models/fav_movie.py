import uuid

from pydantic import BaseModel


class FavMovie(BaseModel):
    """Класс избранного фильма пользователя."""
    id: uuid.UUID
    user_id: uuid.UUID
    movie_id: uuid.UUID
