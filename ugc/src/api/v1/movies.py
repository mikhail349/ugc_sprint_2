from http import HTTPStatus
import uuid

from flask import Blueprint, current_app, request, Response

from src.storages.base import Storage
from src.services.auth import username_required


movies = Blueprint("movies", __name__,  url_prefix="/movies")


@movies.route("/<movie_id>/views", methods=["POST"])
@username_required
def create_view(username: str, movie_id: uuid.UUID):
    """Создать событие просмотра в хранилище."""

    timestamp = request.json.get("timestamp")

    storage: Storage = current_app.config.get("storage")
    storage.create_view_event(username, movie_id, timestamp)

    return Response(status=HTTPStatus.OK)
