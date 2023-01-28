import pytest

from tests.factories.reviews import create_review
from tests.mocks.auth_mock import init_auth, username_required


@pytest.fixture
def review_obj():
    """Создание объекта ревью."""
    return create_review()


@pytest.fixture(scope="session")
def mock_auth(session_mocker):
    session_mocker.patch("src.services.auth.init_auth", new=init_auth)
    return session_mocker.patch(
        "src.services.auth.username_required", new=username_required
    )


@pytest.fixture(scope="session")
def mock_kafka(session_mocker):
    return session_mocker.patch("src.streamers.kafka.Kafka")


@pytest.fixture(scope="session")
def mock_favs_collection(session_mocker):
    return session_mocker.patch(
        "src.storages.mongo.collections.favs.FavsCollection"
    )


@pytest.fixture(scope="session")
def mock_reviews_collection(session_mocker):
    return session_mocker.patch(
        "src.storages.mongo.collections.reviews.ReviewsCollection"
    )


@pytest.fixture(scope="session")
def mock_ratings_collection(session_mocker):
    return session_mocker.patch(
        "src.storages.mongo.collections.ratings.RatingsCollection"
    )


@pytest.fixture(scope="session")
def mock_collections(
    mock_favs_collection,
    mock_reviews_collection,
    mock_ratings_collection,
):
    pass


@pytest.fixture(scope="session")
def mock_mongo(session_mocker):
    return session_mocker.patch("src.storages.mongo.mongo.Mongo")


@pytest.fixture(scope="session")
def mock_redis(session_mocker):
    return session_mocker.patch("src.cache.redis.Redis")


@pytest.fixture(scope="session")
def mock_configs(session_mocker):
    return session_mocker.patch("src.services.sentry.init_sentry")


@pytest.fixture(scope="session")
def app(mock_auth, mock_kafka, mock_redis, mock_collections):
    from src.app.app import app as ugc_app

    with ugc_app.app_context():
        ugc_app.config["DEBUG"] = True
        ugc_app.config["TESTING"] = True
        yield ugc_app


@pytest.fixture(scope="session")
def client(app):
    yield app.test_client()
