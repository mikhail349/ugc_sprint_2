import typing as t

from pydantic import BaseModel


class MovieRating(BaseModel):
    """Модель рейтингов фильма."""
    creator: t.Optional[int] = None
    overall: t.Optional[float] = None


class LikeDislikeRating(BaseModel):
    """Модель с количеством лайков и дизлайков."""
    likes: int = 0
    dislikes: int = 0
