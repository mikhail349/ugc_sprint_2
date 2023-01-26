import logging
from flask import request
from logging.handlers import RotatingFileHandler
from src.configs.logger import logger_config

logger = logging.getLogger(__name__)


class RequestIdFilter(logging.Filter):
    """Класс для добавления в лог информации о request-id,
    с которым был выполнен запрос."""

    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


def init_logger():
    """Инициализировать логирование."""
    global logger
    logging.basicConfig(
        filename=logger_config.file,
        level=logging.INFO,
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addFilter(RequestIdFilter())
    handler = RotatingFileHandler(
        logger_config.file,
        maxBytes=logger_config.file_max_bytes
    )
    logger.addHandler(handler)
    return logger
