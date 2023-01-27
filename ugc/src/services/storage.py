from flask import Flask
import pymongo

from src.storages.mongo.mongo import Mongo
from src.storages.mongo.collections.favs import FavsCollection
from src.storages.mongo.collections.reviews import ReviewsCollection
from src.storages.mongo.collections.ratings import RatingsCollection
from src.configs.mongo import mongo_config


def init_storage(app: Flask) -> None:
    """Инициализировать хранилище.

    Args:
        app: приложение Flask.

    """
    client = pymongo.MongoClient(
        f"mongodb://{mongo_config.host}:{mongo_config.port}"
    )
    db = client[mongo_config.db]

    favs = FavsCollection(db)
    reviews = ReviewsCollection(db)
    ratings = RatingsCollection(db)

    app.config['storage'] = Mongo(
        favs=favs,
        reviews=reviews,
        ratings=ratings
    )
