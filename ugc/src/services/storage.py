from flask import Flask

from src.storages.mongo import Mongo


def init_storage(app: Flask) -> None:
    """Инициализировать хранилище.

    Args:
        app: приложение Flask.

    """
    app.config['storage'] = Mongo()
