from dataclasses import dataclass
import random
import threading
import time
import logging
import uuid

from src.storages.base import Storage
from src.factories.movie import create_movie
from src.factories.user import create_user
from src.factories.fav_movie import create_fav_movie
from src.factories.movie_score import create_movie_score
from src.utils import counter
from src.configs.researcher import researcher_config


@dataclass
class Researcher:
    """Класс исследования хранилища."""
    storage: Storage

    def populate(self):
        """Наполнить хранилище данными."""

        self.users = [
            uuid.uuid4() for _ in range(researcher_config.user_amount)
        ]
        self.movies = [
            uuid.uuid4() for _ in range(researcher_config.movie_amount)
        ]

        self.storage.populate(
            users=self.users,
            fav_movies_per_user=researcher_config.fav_movies_per_user_amount,
            movies=self.movies,
            scores_per_movie=researcher_config.scores_per_movie_amount
        )

    @counter(iterations=researcher_config.read_write_iterations)
    def write_fav_movie(self):
        """Запись избранного фильма."""
        self.storage.add_fav_movie(create_fav_movie())

    @counter(iterations=researcher_config.read_write_iterations)
    def write_movie_score(self):
        """Запись оценки фильма."""
        self.storage.add_movie_score(create_movie_score())

    @counter(iterations=researcher_config.read_write_iterations)
    def read_fav_movies(self):
        """Чтение избранных фильмов пользователей."""
        random_ix = random.randint(0, len(self.users) - 1)
        user = self.users[random_ix]
        self.storage.get_fav_movies(user_id=user)

    @counter(iterations=researcher_config.read_write_iterations)
    def read_movie_score(self):
        """Чтение оценок фильмов."""
        random_ix = random.randint(0, len(self.movies) - 1)
        movie = self.movies[random_ix]
        self.storage.get_movie_score(movie_id=movie)

    @counter(iterations=researcher_config.read_write_iterations)
    def read_write_movie_score(self):
        """Чтение оценок фильмов в реальном времени."""
        def _write():
            while not event.is_set():
                self.storage.add_movie_score(create_movie_score())
                time.sleep(.1)

        def _read():
            user = create_user()
            movie = create_movie()
            self.storage.add_movie_score(
                create_movie_score(
                    user_id=user.id,
                    movie_id=movie.id
                )
            )
            self.storage.get_movie_score(movie_id=movie.id)
            event.set()

        event = threading.Event()
        threads = [
            threading.Thread(target=_write),
            threading.Thread(target=_read)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def perform(self):
        """Запустить измерение."""
        logging.info(f"Research of {self.storage.__class__.__name__}")
        self.populate()
        self.write_fav_movie()
        self.write_movie_score()
        self.read_fav_movies()
        self.read_movie_score()
        self.read_write_movie_score()
