import random
import string

symbols_for_path = string.ascii_letters + string.digits


def get_random_ascii_seq(length: int):
    return "".join(random.choice(symbols_for_path) for i in range(length))  # nosec # noqa: S311
