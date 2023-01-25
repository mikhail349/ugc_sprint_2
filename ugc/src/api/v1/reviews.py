from http import HTTPStatus
import uuid
from typing import Any

from flask import Response, jsonify, request, make_response
from flask_restful import Resource

from src.storages.errors import DuplicateError
from src.storages.base import ReviewSort
from src.api.v1 import messages as msg
from src.api.mixins import StorageMixin, LoginMixin
from src.services.auth import username_required


class Review(StorageMixin, Resource):
    """API ресурс по работе с рецензиями."""

    @username_required
    def post(self, username: str, movie_id: uuid.UUID):
        """Добавить рецензию."""
        text = request.json.get("text")

        try:
            review_id = self.storage.add_review(
                movie_id=movie_id,
                username=username,
                text=text
            )
            return jsonify(id=review_id)
        except DuplicateError:
            return jsonify(msg=msg.REVIEW_EXISTS), HTTPStatus.BAD_REQUEST

    def get(self, movie_id: uuid.UUID):
        """Получить список рецензий.

        Args:
            movie_id: ИД фильма.

        """
        sort = (
            ReviewSort(request.args.get("sort"))
            if "sort" in request.args else None
        )
        reviews = self.storage.get_reviews(movie_id=movie_id, sort=sort)
        return jsonify(reviews)


class ReviewRating(LoginMixin, StorageMixin, Resource):
    """API ресурс по работе с оценками рецензий."""

    def post(self, movie_id: uuid.UUID, review_id: Any):
        """Поставить оценку рецензии."""
        rating = request.json.get("rating")
        try:
            self.storage.add_review_rating(
                review_id=review_id,
                username=self.username,
                rating=rating
            )
        except DuplicateError:
            return make_response(
                jsonify(msg=msg.REVIEW_RATING_EXISTS),
                HTTPStatus.BAD_REQUEST
            )

        return Response(status=HTTPStatus.OK)