from http import HTTPStatus
import uuid

from flask import Blueprint, current_app, request, Response, jsonify

from src.storages.base import Storage
from src.services.auth import username_required
from src.storages.errors import DuplicateError
from src.api.v1 import messages as msg

ratings = Blueprint("ratings", __name__)


@ratings.route("/<movie_id>/ratings", methods=["POST"])
@username_required
def add_rating(username: str, movie_id: uuid.UUID):
    """Поставить оценку фильму."""

    rating = request.json.get("rating")

    storage: Storage = current_app.config.get("storage")
    try:
        storage.add_rating(movie_id=movie_id, username=username, rating=rating)
    except DuplicateError:
        return jsonify(msg=msg.MOVIE_RATING_EXISTS), HTTPStatus.BAD_REQUEST

    return Response(status=HTTPStatus.OK)


@ratings.route("/<movie_id>/ratings", methods=["PUT"])
@username_required
def edit_rating(username: str, movie_id: uuid.UUID):
    """Изменить оценку фильма."""

    rating = request.json.get("rating")

    storage: Storage = current_app.config.get("storage")
    storage.edit_rating(movie_id=movie_id, username=username, rating=rating)

    return Response(status=HTTPStatus.OK)


@ratings.route("/<movie_id>/ratings", methods=["DELETE"])
@username_required
def delete_rating(username: str, movie_id: uuid.UUID):
    """Удалить оценку фильма."""

    storage: Storage = current_app.config.get("storage")
    storage.delete_rating(movie_id=movie_id, username=username)

    return Response(status=HTTPStatus.OK)


@ratings.route("/<movie_id>/ratings", methods=["GET"])
@username_required
def get_rating(username: str, movie_id: uuid.UUID):
    """Получить свою оценку фильма."""

    storage: Storage = current_app.config.get("storage")
    result = storage.get_rating(movie_id=movie_id, username=username)

    return jsonify(rating=result)


@ratings.route("/<movie_id>/ratings/overall", methods=["GET"])
def get_overall_rating(movie_id: uuid.UUID):
    """Получить оценку фильма."""

    storage: Storage = current_app.config.get("storage")
    result = storage.get_overall_rating(movie_id=movie_id)

    return jsonify(rating=result)
