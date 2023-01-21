from http import HTTPStatus
import uuid

from flask import request, Response, jsonify
from flask_restful import Resource

from src.storages.errors import DuplicateError
from src.api.v1 import messages as msg
from src.api.v1.base import StorageMixin, LoginMixin


class Rating(LoginMixin, StorageMixin, Resource):
    """Ресурс по работе с оценкой фильма."""

    def post(self, movie_id: uuid.UUID):
        """Поставить оценку фильму."""

        rating = request.json.get("rating")
        try:
            self.storage.add_rating(
                movie_id=movie_id,
                username=self.username,
                rating=rating
            )
        except DuplicateError:
            return jsonify(msg=msg.MOVIE_RATING_EXISTS), HTTPStatus.BAD_REQUEST

        return Response(status=HTTPStatus.OK)

    def put(self, movie_id: uuid.UUID):
        """Изменить оценку фильма."""

        rating = request.json.get("rating")

        self.storage.edit_rating(
            movie_id=movie_id,
            username=self.username,
            rating=rating
        )

        return Response(status=HTTPStatus.OK)

    def delete_rating(self, movie_id: uuid.UUID):
        """Удалить оценку фильма."""

        self.storage.delete_rating(movie_id=movie_id, username=self.username)
        return Response(status=HTTPStatus.OK)

    def get(self, movie_id: uuid.UUID):
        """Получить свою оценку фильма."""

        result = self.storage.get_rating(
            movie_id=movie_id,
            username=self.username
        )
        return jsonify(rating=result)


class OverallRating(StorageMixin, Resource):
    """Ресурс по работе с общей оценкой фильма."""

    def get(self, movie_id: uuid.UUID):
        """Получить оценку фильма."""

        result = self.storage.get_overall_rating(movie_id=movie_id)
        return jsonify(rating=result)
