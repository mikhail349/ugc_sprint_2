from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka import errors
from kafka.producer.future import FutureRecordMetadata
import backoff

from src.streamers.base import Streamer
from src.configs.kafka import Topic


class Kafka(Streamer):
    """Стример Kafka.

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
    
    @backoff.on_exception(backoff.expo, exception=errors.BrokerResponseError)
    def send(self, topic: Topic, key: str = None, value: str = None):
        """Отправить сообщение в Kafka.

        Args:
            topic: топик класса Topic
            key: ключ
            value: значение

        """
        future: FutureRecordMetadata = self.producer.send(
            topic=topic.value,
            key=key.encode() if key else None,
            value=value.encode() if value else None
        )
        future.get(timeout=self.producer_timeout)

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

    def send_view(self, username: str, movie_id: str, timestamp: int):
        key = f"{username}_{movie_id}"
        value = str(timestamp)
        self.send(
            topic=Topic.VIEWS,
            key=key,
            value=value
        )

    def send_review_rating(self, username: str, review_id: str, rating: int):
        key = f"{username}_{review_id}"
        value = str(rating)
        self.send(
            topic=Topic.RATINGS,
            key=key,
            value=value
        )
