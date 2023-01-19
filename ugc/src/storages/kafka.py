from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka import errors
import backoff

from src.storages.base import Storage
from src.configs.kafka import Topic


class Kafka(Storage):
    """Хранилище Kafka.

    Args:
        servers: перечень серверов в формате host1:port1,host2:port2,...
        producer_timeout: таймаут ожидания на запись
    """

    def __init__(self, servers: str, producer_timeout: int) -> None:
        self.servers = servers.split(",")
        self.producer_timeout = producer_timeout
        self.producer = KafkaProducer(
            bootstrap_servers=self.servers
        )

    @backoff.on_exception(backoff.expo, exception=Exception)
    def create_topic(
        self,
        name: str,
        num_partitions: int = 1,
        replication_factor: int = 1
    ) -> None:
        """Создать топик.

        Args:
            name: имя
            num_partitions: кол-во партиций
            replication_factor: кол-во репликаций

        """
        admin_client = KafkaAdminClient(
            bootstrap_servers=self.servers
        )

        topics = [
            NewTopic(
                name=name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
        ]
        try:
            admin_client.create_topics(new_topics=topics, validate_only=False)
        except errors.TopicAlreadyExistsError:
            pass

    @backoff.on_exception(backoff.expo, exception=Exception)
    def create_view_event(
        self,
        username: str,
        movie_id: str,
        timestamp: int
    ) -> None:
        key = f"{username}_{movie_id}"
        value = str(timestamp)
        future = self.producer.send(
            topic=Topic.VIEWS.value,
            key=key.encode(),
            value=value.encode(),
        )
        future.get(timeout=self.producer_timeout)
