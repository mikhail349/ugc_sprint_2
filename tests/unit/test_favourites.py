import uuid
from http import HTTPStatus

from src.storages.errors import DuplicateError

from tests.constants import urls
from tests.constants.test_user import USERNAME
from tests.utils.string_utils import generate_random_string


class TestFavourites:
    def test_post(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        res = client.post(urls.MOVIE_IN_FAVOURITES.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        mock_mongo.return_value.add_to_fav.assert_called_with(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_post_duplicate(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        mock_mongo.return_value.add_to_fav.side_effect = DuplicateError()
        res = client.post(urls.MOVIE_IN_FAVOURITES.format(movie_uuid))
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.add_to_fav.assert_called_with(
            movie_id=movie_uuid, username=USERNAME
        )
        mock_mongo.return_value.add_to_fav.side_effect = None

    def test_delete(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())
        res = client.delete(urls.MOVIE_IN_FAVOURITES.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        mock_mongo.return_value.delete_from_fav.assert_called_with(
            movie_id=movie_uuid, username=USERNAME
        )

    def test_get(self, mock_mongo, client):
        expected_value = generate_random_string()
        mock_mongo.return_value.get_favs.return_value = expected_value
        res = client.get(urls.FAVOURITES_LIST)
        assert res.status_code == HTTPStatus.OK
        assert res.json == expected_value
        mock_mongo.return_value.get_favs.assert_called_with(username=USERNAME)
