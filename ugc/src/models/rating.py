from typing import Optional

from pydantic import BaseModel


class MovieRating(BaseModel):
    """Модель рейтингов фильма."""
    creator: Optional[int] = None
    overall: Optional[float] = None


class LikeDislikeRating(BaseModel):
    """Модель с количеством лайков и дизлайков."""
    likes: int = 0
    dislikes: int = 0
