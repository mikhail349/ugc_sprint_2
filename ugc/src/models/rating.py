from pydantic import BaseModel


class MovieRating(BaseModel):
    """Модель рейтингов фильма."""
    creator: int = None
    overall: float = None


class LikeDislikeRating(BaseModel):
    """Модель с количеством лайков и дизлайков."""
    likes: int = 0
    dislikes: int = 0
