import json
import random
import uuid
from http import HTTPStatus

from src.storages.errors import DoesNotExistError, DuplicateError

from tests.constants import urls
from tests.constants.test_user import USERNAME


class TestRatings:
    def test_post(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)

        data = json.dumps(dict(rating=rating))
        res = client.post(
            urls.RATINGS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.OK
        mock_mongo.return_value.add_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME, rating=rating
        )

    def test_post_duplicate(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)
        mock_mongo.return_value.add_rating.side_effect = DuplicateError()
        data = json.dumps(dict(rating=rating))
        res = client.post(
            urls.RATINGS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.add_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME, rating=rating
        )
        mock_mongo.return_value.add_rating.side_effect = None

    def test_put(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)
        data = json.dumps(dict(rating=rating))
        res = client.put(
            urls.RATINGS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.OK
        mock_mongo.return_value.edit_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME, rating=rating
        )

    def test_put_does_not_exist(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)
        mock_mongo.return_value.edit_rating.side_effect = DoesNotExistError()
        data = json.dumps(dict(rating=rating))
        res = client.put(
            urls.RATINGS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.edit_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME, rating=rating
        )
        mock_mongo.return_value.edit_rating.side_effect = None

    def test_delete(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        res = client.delete(urls.RATINGS.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        mock_mongo.return_value.delete_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_delete_does_not_exist(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        mock_mongo.return_value.delete_rating.side_effect = DoesNotExistError()
        res = client.delete(urls.RATINGS.format(movie_uuid))
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.delete_rating.assert_called_with(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_get(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)
        mock_mongo.return_value.get_rating.return_value = rating
        res = client.get(urls.RATINGS.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        assert res.json == {"rating": rating}
        mock_mongo.return_value.delete_rating.get_rating(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_get_does_not_exist(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        mock_mongo.return_value.get_rating.side_effect = DoesNotExistError()
        res = client.get(urls.RATINGS.format(movie_uuid))
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.delete_rating.get_rating(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_get_overall(self, mock_mongo, mock_redis, client):
        movie_uuid = str(uuid.uuid4())
        rating = random.randint(0, 10)
        mock_mongo.return_value.get_overall_rating.return_value = rating
        mock_redis.return_value.get.return_value = None
        res = client.get(urls.OVERALL_RATINGS.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        assert res.json == {"rating": rating}
        mock_mongo.return_value.delete_rating.get_rating(
            movie_id=movie_uuid, username=USERNAME
        )
