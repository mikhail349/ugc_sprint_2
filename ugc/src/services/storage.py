from flask import Flask
import pymongo

from src.storages.mongo.mongo import Mongo
from src.storages.mongo.collections.favs_collection import FavsCollection
from src.configs.mongo import mongo_config


def init_storage(app: Flask) -> None:
    """Инициализировать хранилище.

    Args:
        app: приложение Flask.

    """
    client = pymongo.MongoClient(f"mongodb://{mongo_config.host}:{mongo_config.port}")
    db = client[mongo_config.db]
    favs_coll = FavsCollection(db)
    app.config['storage'] = Mongo(db=db, favs=favs_coll)
