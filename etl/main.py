import logging
import time
import uuid

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from etl.configs import clickhouse_config, kafka_config, etl_config


@backoff.on_exception(wait_gen=backoff.expo, exception=Exception)
def load_views_to_clickhouse(data) -> None:
    """Загружает данные в clickhouse."""
    clickhouse_client.execute(
        f"INSERT INTO {clickhouse_config.db_name}.{clickhouse_config.table_name} "  # noqa: E501
        f"(id, user_id, movie_id, timestamp) VALUES",
        data,
    )
    logging.info(f"{len(data)} record(s) loaded to clickhouse")


@backoff.on_exception(wait_gen=backoff.expo, exception=Exception)
def load_data_kafka_to_clickhouse() -> None:
    """Переносит данные из kafka в clickhouse."""
    start_time = time.time()
    data_batch = []
    for message in kafka_consumer:
        user_id, movie_id = message.key.decode().split("_")
        data_batch.append(
            (str(uuid.uuid4()), user_id, movie_id, int(message.value.decode()))
        )
        if (
            len(data_batch) > etl_config.batch_size
            or time.time() - start_time > etl_config.max_timeout
        ):
            load_views_to_clickhouse(data_batch)
            start_time = time.time()
            data_batch = []
            kafka_consumer.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    kafka_consumer = KafkaConsumer(
        kafka_config.topic_name,
        bootstrap_servers=kafka_config.servers.split(","),
        auto_offset_reset="earliest",
        group_id="etl",
        enable_auto_commit=False,
    )
    clickhouse_client = Client(host=clickhouse_config.host)
    try:
        load_data_kafka_to_clickhouse()
    except Error as e:
        logging.error(f"Clickhouse error: {e}")
    except KafkaError as e:
        logging.error(f"Kafka error: {e}")
