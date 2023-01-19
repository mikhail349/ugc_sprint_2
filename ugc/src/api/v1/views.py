from http import HTTPStatus

from flask import Blueprint, current_app, request, Response

from src.storages.base import Storage
from src.services.auth import username_required


views = Blueprint("views", __name__,  url_prefix="/views")


@views.route("/", methods=["POST"])
@username_required
def create_view_event(username: str):
    """Создать событие просмотра в хранилище."""

    movie_id = request.json.get("movie_id")
    timestamp = request.json.get("timestamp")

    storage: Storage = current_app.config.get("storage")
    storage.create_view_event(username, movie_id, timestamp)

    return Response(status=HTTPStatus.OK)
