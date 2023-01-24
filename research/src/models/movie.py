import uuid

from pydantic import BaseModel


class Movie(BaseModel):
    """Класс фильма."""
    id: uuid.UUID
    name: str
