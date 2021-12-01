__all__ = [
    "DEBUG",
    "flatten",
    "debug_print",
    "getlines",
    "get_day"
]

import os
import sys
from itertools import chain

import requests as requests

gettrace = getattr(sys, 'gettrace', bool)

DEBUG = bool(gettrace())

flatten = chain.from_iterable


def debug_print(*args, **kwargs):
    if DEBUG:
        return print(*args, **kwargs)


def getlines(data: str, test_data: str, sep: str = "\n"):
    if DEBUG:
        return test_data.rstrip().split(sep)
    else:
        return data.rstrip().split(sep)


def get_day(day: int, year=2021) -> str:
    filename = f"input{day:02d}.txt"
    if os.path.exists(filename):
        with open(filename) as cache_file:
            return cache_file.read()
    with open(".token", "r") as token_file:
        cookies = {"session": token_file.read().strip()}
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
        with open(filename, "w") as cache_file:
            cache_file.write(response.text.strip())
        return response.text.strip()
