import time
import functools
import logging


def counter(iterations: int = 1):
    """Декоратор замера скорости выполнения функции.

    Args:
        iterations: кол-во вызовов функции

    """
    def inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            timers = []
            logging.info(f"{f.__name__}")

            for _ in range(iterations):
                start = time.perf_counter()
                result = f(*args, **kwargs)
                end = time.perf_counter()
                timers.append(end - start)

            seconds = sum(timers) / len(timers)
            logging.info(
                f"Done in {seconds} seconds average "
                f"within {iterations} iterations."
            )
            return result
        return wrapper
    return inner
