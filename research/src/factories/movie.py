import uuid

from faker import Faker

from src.models.movie import Movie

fake = Faker()


def create_movie() -> Movie:
    """Создать фильм."""
    return Movie(
        id=uuid.uuid4(),
        name=fake.word()
    )
