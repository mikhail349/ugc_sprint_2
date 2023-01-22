from http import HTTPStatus
import uuid

from flask import Response, jsonify, request
from flask_restful import Resource

from src.storages.errors import DuplicateError
from src.api.v1 import messages as msg
from src.api.v1.base import StorageMixin
from src.services.auth import username_required


class Review(StorageMixin, Resource):
    """API ресурс по работе с рецензиями."""

    @username_required
    def post(self, username: str, movie_id: uuid.UUID):
        """Добавить рецензию."""
        text = request.json.get("text")

        try:
            self.storage.add_review(
                movie_id=movie_id,
                username=username,
                text=text
            )
        except DuplicateError:
            return jsonify(msg=msg.REVIEW_EXISTS), HTTPStatus.BAD_REQUEST

        return Response(status=HTTPStatus.OK)

    def get(self, movie_id: uuid.UUID):
        """Получить список рецензий.

        Args:
            movie_id: ИД фильма.

        """
        return jsonify(self.storage.get_reviews(movie_id=movie_id))
