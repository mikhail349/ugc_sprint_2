from flask import Flask

from src.storages.kafka import Kafka
from src.configs.kafka import kafka_config


def init_storage(app: Flask) -> None:
    """Инициализировать хранилище.

    Args:
        app: приложение Flask.

    """
    kafka = Kafka(servers=kafka_config.servers,
                  producer_timeout=kafka_config.producer_timeout)

    for name, config in kafka_config.topics.items():
        kafka.create_topic(
            name=name,
            num_partitions=config["num_partitions"],
            replication_factor=config["replication_factor"]
        )
    app.config['storage'] = kafka
