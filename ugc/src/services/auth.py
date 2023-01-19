import functools

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from src.configs.jwt import jwt_config


def init_auth(app: Flask):
    """Инициализировать модуль аутентификации.

    Args:
        app: приложение Flask

    """
    app.config.from_mapping(jwt_config.uppercased_dict())
    app.config['JWT_PUBLIC_KEY'] = open(jwt_config.jwt_public_key_path).read()
    jwt = JWTManager()
    jwt.init_app(app)


def username_required(endpoint):
    """Декоратор доступа, который в endpoint передает username."""
    @functools.wraps(endpoint)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        return endpoint(username=identity, *args, **kwargs)
    return wrapper
