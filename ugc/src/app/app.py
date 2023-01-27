from flask import Blueprint, Flask
from src.api.v1.movies import movies
from src.api.v1.openapi import openapi
from src.services.auth import init_auth
from src.services.logger import init_logger
from src.services.sentry import init_sentry
from src.services.storage import init_storage
from src.services.streamer import init_streamer
from src.services.cache import init_cache
from src.utils.encoders import JSONEncoder

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config["PROPAGATE_EXCEPTIONS"] = True


init_auth(app)
init_streamer(app)
init_storage(app)
init_cache(app)
init_logger()
init_sentry()


api = Blueprint("api", __name__, url_prefix="/api")
api_v1 = Blueprint("v1", __name__, url_prefix="/v1")
api_v1.register_blueprint(movies)
api_v1.register_blueprint(openapi)
api.register_blueprint(api_v1)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)
