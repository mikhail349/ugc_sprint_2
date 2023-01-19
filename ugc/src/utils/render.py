import yaml
from flask import render_template


def render_schema(filename: str) -> str:
    """Рендер html со схемой.

    Args:
        filename: имя файла

    Returns:
        str: сгенерированный html

    """
    with open(filename, "r", encoding="utf8") as stream:
        try:
            spec = yaml.safe_load(stream)
            return render_template("swagger.html", spec=spec)
        except yaml.YAMLError:
            return "Error"
