from flask import Flask

from src.storages.mongo import Mongo
from src.configs.mongo import mongo_config


def init_storage(app: Flask) -> None:
    """Инициализировать хранилище.

    Args:
        app: приложение Flask.

    """
    app.config['storage'] = Mongo(**mongo_config.dict())
