from typing import Any
from enum import Enum

from pydantic import Field

from src.configs.base import BaseConfig


class Topic(str, Enum):
    """Перечисление топиков."""
    VIEWS = "views"


class KafkaConfig(BaseConfig):
    """Настройки Kafka."""

    servers: str = Field("127.0.0.1:9092,127.0.0.1:9093", env="KAFKA_SERVERS")
    """Перечень серверов в формате host1:port1,host2:port2,... """
    producer_timeout: int = Field(60, env="KAFKA_PRODUCER_TIMEOUT")
    """Таймаут ожидания на запись."""
    topics: dict[str, dict[str, Any]] = Field(default_factory=dict)
    """Топики."""

    def config_topic(
        self,
        name: str,
        num_partitions: int = 1,
        replication_factor: int = 1
    ) -> None:
        """Настроить топик.

        Args:
            name: имя
            num_partitions: кол-во партиций
            replication_factor: кол-во репликаций

        """
        self.topics[name] = {
            "num_partitions": num_partitions,
            "replication_factor": replication_factor
        }


kafka_config = KafkaConfig()
kafka_config.config_topic(Topic.VIEWS.value)
