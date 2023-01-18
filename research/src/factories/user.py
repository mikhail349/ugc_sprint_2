import uuid

from faker import Faker

from src.models.user import User

fake = Faker()


def create_user() -> User:
    """Создать рандомного пользователя."""
    return User(
        id=uuid.uuid4(),
        username=fake.email()
    )
