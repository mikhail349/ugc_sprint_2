import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
"""Путь до корня проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


class KafkaConfig(BaseConfig):
    """Настройки Kafka."""

    servers: str = Field("127.0.0.1:9092,127.0.0.1:9093", env="KAFKA_SERVERS")
    """Перечень серверов в формате host1:port1,host2:port2,... """
    topic_name: str = "views"
    """Название топика."""


class ClickhouseConfig(BaseConfig):
    """Настройки clickhouse."""

    host: str = Field("127.0.0.1", env="CLICKHOUSE_HOST")
    """Хост для подключения."""
    db_name: str = "default"
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


class LoggerConfig(BaseConfig):
    """Настройки логирования."""

    file: str = Field("logs/app.log", env="LOG_FILE")
    """Имя файла для записи логов."""
    file_max_bytes: int = Field(1000, env="LOG_FILE_MAX_BYTES")
    """Максимальный размер файла для записи логов."""


kafka_config = KafkaConfig()
clickhouse_config = ClickhouseConfig()
etl_config = ETLConfig()
logger_config = LoggerConfig()
