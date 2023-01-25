from http import HTTPStatus
import uuid

from flask import request, Response, jsonify, make_response
from flask_restful import Resource

from src.storages.errors import DuplicateError, DoesNotExistError
from src.api.v1 import messages as msg
from src.api.mixins import StorageMixin, LoginMixin
from src.services.logger import logger


class Rating(LoginMixin, StorageMixin, Resource):
    """API ресурс по работе с оценкой фильма."""

    def post(self, movie_id: uuid.UUID):
        """Поставить оценку фильму."""

        rating = request.json.get("rating")
        try:
            self.storage.add_rating(
                movie_id=movie_id,
                username=self.username,
                rating=rating
            )
            logger.info("Movie rating is created")
        except DuplicateError:
            return make_response(
                jsonify(msg=msg.MOVIE_RATING_EXISTS),
                HTTPStatus.BAD_REQUEST
            )

        return Response(status=HTTPStatus.OK)

    def put(self, movie_id: uuid.UUID):
        """Изменить оценку фильма."""

        rating = request.json.get("rating")
        try:
            self.storage.edit_rating(
                movie_id=movie_id,
                username=self.username,
                rating=rating
            )
            logger.info("Movie rating is updated")
        except DoesNotExistError:
            return make_response(
                jsonify(msg=msg.MOVIE_RATING_DOES_NOT_EXIST),
                HTTPStatus.BAD_REQUEST
            )

        return Response(status=HTTPStatus.OK)

    def delete(self, movie_id: uuid.UUID):
        """Удалить оценку фильма."""
        try:
            self.storage.delete_rating(
                movie_id=movie_id,
                username=self.username
            )
            logger.info("Movie rating is deleted")
        except DoesNotExistError:
            return make_response(
                jsonify(msg=msg.MOVIE_RATING_DOES_NOT_EXIST),
                HTTPStatus.BAD_REQUEST
            )

        return Response(status=HTTPStatus.OK)

    def get(self, movie_id: uuid.UUID):
        """Получить свою оценку фильма."""
        try:
            result = self.storage.get_rating(
                movie_id=movie_id,
                username=self.username
            )
        except DoesNotExistError:
            return make_response(
                jsonify(msg=msg.MOVIE_RATING_DOES_NOT_EXIST),
                HTTPStatus.BAD_REQUEST
            )

        return jsonify(rating=result)


class OverallRating(StorageMixin, Resource):
    """API ресурс по работе с общей оценкой фильма."""

    def get(self, movie_id: uuid.UUID):
        """Получить общую оценку фильма."""

        result = self.storage.get_overall_rating(movie_id=movie_id)
        return jsonify(rating=result)
