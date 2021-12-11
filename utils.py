__all__ = [
    "DEBUG",
    "flatten",
    "debug_print",
    "get_day"
]

import os
import sys
from itertools import chain

import requests as requests

DEBUG = bool(sys.gettrace())

flatten = chain.from_iterable


def debug_print(*args, **kwargs):
    if DEBUG:
        return print(*args, **kwargs)


def get_day(day: int, practice: str = "", year: int = 2021) -> str:
    if DEBUG:
        return practice.strip()
    filename = f"input{day:02d}.txt"
    if not os.path.exists(filename):
        with open(".token", "r") as token_file:
            cookies = {"session": token_file.read().strip()}
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
        with open(filename, "w") as cache_file:
            cache_file.write(response.text.strip())
    with open(filename) as cache_file:
        return cache_file.read().strip()
