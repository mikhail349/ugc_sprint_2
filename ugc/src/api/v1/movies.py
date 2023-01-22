from flask import Blueprint
from flask_restful import Api

from src.api.v1.views import View
from src.api.v1.ratings import Rating, OverallRating
from src.api.v1.favs import FavMovie, FavMovieList
from src.api.v1.reviews import Review


movies = Blueprint("movies", __name__,  url_prefix="/movies")

api = Api(movies)
api.add_resource(View, "/<movie_id>/views")
api.add_resource(Rating, "/<movie_id>/ratings")
api.add_resource(OverallRating, "/<movie_id>/ratings/overall")

api.add_resource(FavMovie, "/<movie_id>/favs")
api.add_resource(FavMovieList, "/favs")

api.add_resource(Review, "/<movie_id>/reviews")
