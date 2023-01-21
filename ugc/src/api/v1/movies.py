from flask import Blueprint
from flask_restful import Api

from src.api.v1.views import View
from src.api.v1.ratings import Rating, OverallRating


movies = Blueprint("movies", __name__,  url_prefix="/movies")

api = Api(movies)
api.add_resource(View, "/<movie_id>/views")
api.add_resource(Rating, "/<movie_id>/ratings")
api.add_resource(OverallRating, "/<movie_id>/ratings/overall")
