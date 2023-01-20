from flask import Blueprint

from src.api.v1.views import views
from src.api.v1.ratings import ratings


movies = Blueprint("movies", __name__,  url_prefix="/movies")
movies.register_blueprint(views)
movies.register_blueprint(ratings)
