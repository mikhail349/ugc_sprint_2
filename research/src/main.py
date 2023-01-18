import logging
import sys

from src.storages.mongo import Mongo
from src.storages.clickhouse import Clickhouse
from src.researcher import Researcher

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    storages = [Clickhouse(), Mongo()]
    for storage in storages:
        researcher = Researcher(storage)
        researcher.perform()


if __name__ == '__main__':
    main()
