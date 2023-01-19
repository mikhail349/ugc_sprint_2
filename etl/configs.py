import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
"""Путь до корня проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


class KafkaConfig(BaseConfig):
    """Настройки Kafka."""

    host: str = Field("127.0.0.1", env="KAFKA_HOST")
    """Хост для подключения."""
    port: int = Field(9092, env="KAFKA_PORT")
    """Порт для подключения."""
    topic_name: str = "views"
    """Название топика."""


class ClickhouseConfig(BaseConfig):
    """Настройки clickhouse."""

    host: str = Field("127.0.0.1", env="CLICKHOUSE_HOST")
    """Хост для подключения."""
    db_name: str = "movies"
    """Название базы данных."""
    table_name = "views"
    """Название таблицы."""
    cluster_name = "company_cluster"
    """Название кластера."""


class ETLConfig(BaseConfig):
    """Настройки ETL."""

    batch_size: int = Field(100, env="BATCH_SIZE")
    """Количество записей для загрузки в clickhouse."""
    max_timeout: int = Field(100, env="MAX_TIMEOUT")
    """Максимальное время секундах до загрузки данных в clickhouse."""


kafka_config = KafkaConfig()
clickhouse_config = ClickhouseConfig()
etl_config = ETLConfig()
