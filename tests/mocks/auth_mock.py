import functools

from flask import Flask

from tests.constants.test_user import USERNAME


def init_auth(app: Flask):
    pass


def username_required(endpoint):
    @functools.wraps(endpoint)
    def wrapper(*args, **kwargs):
        return endpoint(username=USERNAME, *args, **kwargs)

    return wrapper
