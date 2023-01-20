from http import HTTPStatus
import uuid

from flask import Blueprint, current_app, request, Response

from src.streamers.base import Streamer
from src.services.auth import username_required

views = Blueprint("views", __name__)


@views.route("/<movie_id>/views", methods=["POST"])
@username_required
def send_view(username: str, movie_id: uuid.UUID):
    """Отправить событие просмотра в стример событий."""

    timestamp = request.json.get("timestamp")

    streamer: Streamer = current_app.config.get("streamer")
    streamer.send_view(username, movie_id, timestamp)

    return Response(status=HTTPStatus.OK)
