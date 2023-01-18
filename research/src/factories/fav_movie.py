import uuid

from src.models.fav_movie import FavMovie


def create_fav_movie(
    user_id: uuid.UUID | None = None,
    movie_id: uuid.UUID | None = None
) -> FavMovie:
    """Создать рандомный избранный фильм.

    Args:
        user_id: ИД пользователя. По умолчанию рандом.
        movie_id: ИД фильма. По умолчанию рандом.

    """
    return FavMovie(
        id=uuid.uuid4(),
        user_id=user_id or uuid.uuid4(),
        movie_id=movie_id or uuid.uuid4()
    )
