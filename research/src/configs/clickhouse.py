from pydantic import Field

from src.configs.base import BaseConfig


class ClickhouseConfig(BaseConfig):
    """Настройки подключения к Clickhouse."""

    host: str = Field("127.0.0.1", env="CLICKHOUSE_HOST")
    """Хост для подключения."""
    db_name: str = Field("default", env="CLICKHOUSE_DB")
    """Название базы данных."""
    cluster_name = Field("company_cluster", env="CLICKHOUSE_CLUSTER")
    """Название кластера."""
    """ИД строки для чтения."""
    batch_size: int = Field(1000, env="CLICKHOUSE_BATCH_SIZE")
    """Размер пакета для вставки."""


clickhouse_config = ClickhouseConfig()
