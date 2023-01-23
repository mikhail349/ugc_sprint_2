from http import HTTPStatus
import uuid

from flask import Response, jsonify
from flask_restful import Resource

from src.storages.errors import DuplicateError
from src.api.v1 import messages as msg
from src.api.mixins import StorageMixin, LoginMixin


class FavMovie(LoginMixin, StorageMixin, Resource):
    """API ресурс по работе с избранными фильмам."""

    def post(self, movie_id: uuid.UUID):
        """Добавить фильм в избранное."""

        try:
            self.storage.add_to_fav(movie_id=movie_id, username=self.username)
        except DuplicateError:
            return jsonify(msg=msg.FAV_MOVIE_EXISTS), HTTPStatus.BAD_REQUEST

        return Response(status=HTTPStatus.OK)

    def delete(self, movie_id: uuid.UUID):
        """Удалить фильм из избранного."""

        self.storage.delete_from_fav(movie_id=movie_id, username=self.username)
        return Response(status=HTTPStatus.OK)


class FavMovieList(LoginMixin, StorageMixin, Resource):
    """API ресурс по работе с общей оценкой фильма."""

    def get(self):
        """Получить список избранных фильмов."""

        result = self.storage.get_favs(username=self.username)
        return jsonify(result)
