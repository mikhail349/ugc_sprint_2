import uuid
import random

from src.models.movie_score import MovieScore


def create_movie_score(
    user_id: uuid.UUID | None = None,
    movie_id: uuid.UUID | None = None,
    score: int | None = None
) -> MovieScore:
    """Создать оценку фильма.

    Args:
        user_id: ИД фильма. По умолчанию - рандом
        movie_id: ИД фильма. По умолчанию - рандом
        score: Оценка. По умолчанию - рандом

    """
    return MovieScore(
        id=uuid.uuid4(),
        user_id=user_id or uuid.uuid4(),
        movie_id=movie_id or uuid.uuid4(),
        score=score or random.randint(0, 10)
    )
