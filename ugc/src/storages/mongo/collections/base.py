from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation

from pymongo.collection import Collection as MongoCollection
from pymongo.database import Database as MongoDatabase


class BaseCollection:
    """Базовый класс коллекции Mongo.

    Args:
        db: База данных Mongo

    """

    def __init__(self, db: MongoDatabase) -> None:
        self.db = db

    def get_collection(self, name: str) -> MongoCollection:
        """Получить коллекцию MongoDB с кодеком UUID.

        Args:
            name: название коллекции

        Returns:
            MongoCollection: коллекция pymongo

        """
        return self.db.get_collection(
            name=name,
            codec_options=CodecOptions(
                uuid_representation=UuidRepresentation.STANDARD
            )
        )
