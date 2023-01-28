import random
import string


def generate_random_string(length: int = 10) -> str:
    """Возвращает случайную строку заданной длины."""
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for _ in range(length))
