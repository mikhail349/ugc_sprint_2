from http import HTTPStatus
import uuid

from flask import request, Response
from flask_restful import Resource

from src.api.mixins import StreamerMixin, LoginMixin


class View(LoginMixin, StreamerMixin, Resource):
    """API ресурс по работе с событиями просмотра фильма."""

    def post(self, movie_id: uuid.UUID):
        """Отправить событие просмотра в стример событий."""

        timestamp = request.json.get("timestamp")
        self.streamer.send_view(self.username, movie_id, timestamp)
        return Response(status=HTTPStatus.OK)
