import logging
from logging.handlers import RotatingFileHandler
from etl.configs import logger_config

logger = logging.getLogger(__name__)


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
    handler = RotatingFileHandler(
        logger_config.file,
        maxBytes=logger_config.file_max_bytes
    )
    logger.addHandler(handler)
    return logger
