import uuid

from pydantic import BaseModel


class User(BaseModel):
    """Класс пользователя."""
    id: uuid.UUID
    username: str
