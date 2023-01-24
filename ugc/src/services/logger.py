import logging
from flask import Flask, request


class RequestIdFilter(logging.Filter):
    """Класс для добавления в лог информации о request-id, с которым был выполнен запрос."""

    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


def init_logger(app: Flask):
    """Инициализировать модуль логирования.

    Args:
        app: приложение Flask

    """

    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
    )

    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    app.logger.addFilter(RequestIdFilter())
