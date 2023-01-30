import json
import random
import uuid
from http import HTTPStatus

from tests.constants import urls
from tests.constants.test_user import USERNAME


class TestView:
    def test_post(self, client, mock_kafka, mock_mongo):
        movie_uuid = str(uuid.uuid4())
        timestamp = random.randrange(5_000)
        data = json.dumps(dict(timestamp=timestamp))
        res = client.post(
            urls.VIEWS.format(movie_uuid),
            data=data,
            content_type="application/json",
        )
        assert res.status_code == HTTPStatus.OK
        mock_kafka.return_value.send_view.assert_called_once_with(
            USERNAME, movie_uuid, timestamp
        )
