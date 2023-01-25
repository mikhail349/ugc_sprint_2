import logging
from flask import request


class RequestIdFilter(logging.Filter):
    """Класс для добавления в лог информации о request-id,
    с которым был выполнен запрос."""

    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


def init_logger():
    """Инициализировать логирование."""
    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addFilter(RequestIdFilter())
    return logger


logger = init_logger()