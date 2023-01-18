import logging
import sys

from src.storages.mongo import MongoStorage
from src.researcher import Researcher

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    storages = [MongoStorage()]
    for storage in storages:
        researcher = Researcher(storage)
        researcher.perform()


if __name__ == '__main__':
    main()
