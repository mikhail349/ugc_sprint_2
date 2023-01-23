from flask import Blueprint, Flask

from src.api.v1.movies import movies
from src.api.v1.openapi import openapi

from src.services.auth import init_auth
from src.services.streamer import init_streamer
from src.services.storage import init_storage
from src.utils.encoders import JSONEncoder


app = Flask(__name__)
app.json_encoder = JSONEncoder
init_auth(app)
init_streamer(app)
init_storage(app)


api = Blueprint("api", __name__, url_prefix="/api")
api_v1 = Blueprint("v1", __name__, url_prefix="/v1")
api_v1.register_blueprint(movies)
api_v1.register_blueprint(openapi)
api.register_blueprint(api_v1)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)
