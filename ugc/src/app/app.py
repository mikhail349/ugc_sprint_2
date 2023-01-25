import sentry_sdk
from flask import Blueprint, Flask, request
from src.api.v1.movies import movies
from src.api.v1.openapi import openapi
from src.configs.sentry import sentry_config
from src.services.auth import init_auth
from src.services.logger import init_logger
from src.services.storage import init_storage
from src.services.streamer import init_streamer
from src.utils.encoders import JSONEncoder

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config['PROPAGATE_EXCEPTIONS'] = True

sentry_sdk.init(
    dsn=sentry_config.dsn,
    traces_sample_rate=sentry_config.traces_sample_rate
)

init_auth(app)
init_streamer(app)
init_storage(app)
init_logger(app)


api = Blueprint("api", __name__, url_prefix="/api")
api_v1 = Blueprint("v1", __name__, url_prefix="/v1")
api_v1.register_blueprint(movies)
api_v1.register_blueprint(openapi)
api.register_blueprint(api_v1)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)
