import uuid
from datetime import datetime

from src.models.rating import LikeDislikeRating, MovieRating
from src.models.review import Review
from tests.constants.test_user import USERNAME

from tests.utils.string_utils import generate_random_string


def create_review() -> Review:
    """Создание рандомного объекта ревью.

    Returns: Review
    """
    return Review(
        id=uuid.uuid4(),
        creator=USERNAME,
        movie_id=uuid.uuid4(),
        text=generate_random_string(),
        created_at=datetime.now().isoformat(),
        movie_rating=MovieRating(),
        review_rating=LikeDislikeRating(),
    )
