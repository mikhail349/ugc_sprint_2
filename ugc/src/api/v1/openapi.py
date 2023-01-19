import os

from flask import Blueprint

from src.configs.base import BASE_DIR
from src.utils.render import render_schema


openapi = Blueprint("openapi", __name__, url_prefix="/openapi")


@openapi.route("/", methods=["GET"])
def schema():
    filename = os.path.join(BASE_DIR, "src/api/v1/", "schema.yaml")
    return render_schema(filename)
