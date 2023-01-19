from flask import Blueprint, Flask

from src.api.v1.views import views
from src.api.v1.openapi import openapi
from src.services.auth import init_auth
from src.services.storage import init_storage


app = Flask(__name__)
init_auth(app)
init_storage(app)

api = Blueprint("api", __name__, url_prefix="/api")
api_v1 = Blueprint("v1", __name__, url_prefix="/v1")
api_v1.register_blueprint(views)
api_v1.register_blueprint(openapi)
api.register_blueprint(api_v1)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)
