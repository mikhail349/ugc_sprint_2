import json
import random
import uuid
from http import HTTPStatus

from src.storages.errors import DuplicateError

from tests.constants import urls
from tests.constants.test_user import USERNAME
from tests.utils.string_utils import generate_random_string


class TestReview:
    def test_post_review_rating(self, mock_mongo, mock_kafka, client):
        review_id = str(uuid.uuid4())
        rating = random.randint(0, 10)
        data = json.dumps(dict(rating=rating))
        res = client.post(
            urls.REVIEW_RATINGS.format(review_id),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.OK
        mock_kafka.return_value.send_review_rating.assert_called_with(
            review_id=review_id, username=USERNAME, rating=rating
        )
        mock_mongo.return_value.add_review_rating.assert_called()

    def test_post_duplicate_review_rating(
        self, mock_mongo, mock_kafka, client
    ):
        mock_kafka.return_value.send_review_rating.side_effect = (
            DuplicateError()
        )
        review_id = str(uuid.uuid4())
        rating = random.randint(0, 10)
        data = json.dumps(dict(rating=rating))
        res = client.post(
            urls.REVIEW_RATINGS.format(review_id),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_kafka.return_value.send_review_rating.assert_called_with(
            review_id=review_id, username=USERNAME, rating=rating
        )
        mock_mongo.return_value.add_review_rating.assert_called()
        mock_kafka.return_value.send_review_rating.side_effect = None

    def test_post_review(self, mock_mongo, client):
        expected_id = str(uuid.uuid4())
        movie_uuid = str(uuid.uuid4())
        mock_mongo.return_value.add_review.return_value = expected_id
        data = json.dumps(dict(text=generate_random_string()))
        res = client.post(
            urls.REVIEWS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.OK
        assert res.json == {"id": expected_id}
        mock_mongo.return_value.add_review.assert_called()

    def test_post_review_duplicate(self, mock_mongo, client):
        movie_uuid = str(uuid.uuid4())

        mock_mongo.return_value.add_review.side_effect = DuplicateError()
        data = json.dumps(dict(text=generate_random_string()))
        res = client.post(
            urls.REVIEWS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.BAD_REQUEST
        mock_mongo.return_value.add_review.assert_called()
        mock_mongo.return_value.add_review.side_effect = None

    def test_get_reviews(self, mock_mongo, client, review_obj):
        movie_uuid = str(uuid.uuid4())
        mock_mongo.return_value.get_reviews.return_value = [review_obj]
        res = client.get(urls.REVIEWS.format(movie_uuid))
        assert res.status_code == HTTPStatus.OK
        assert res.json == [json.loads(review_obj.json())]
        mock_mongo.return_value.get_reviews.assert_called()
