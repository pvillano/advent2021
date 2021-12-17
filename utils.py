__all__ = [
    "benchmark",
    "DEBUG",
    "debug_print",
    "debug_print_grid",
    "flatten",
    "get_day",
    "pipe",
]

import os
import sys
import time
from itertools import chain

import requests as requests

DEBUG = bool(sys.gettrace())

flatten = chain.from_iterable


def debug_print(*args, **kwargs):
    if DEBUG:
        return print(*args, **kwargs, file=sys.stderr, flush=True)


def get_day(day: int, practice: str = "", *, year: int = 2021, override=False) -> str:
    if DEBUG and not override:
        return practice.strip()
    filename = f"input{day:02d}.txt"
    if not os.path.exists(filename):
        with open(".token", "r") as token_file:
            cookies = {"session": token_file.read().strip()}
        response = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies
        )
        with open(filename, "w") as cache_file:
            cache_file.write(response.text.strip())
    with open(filename) as cache_file:
        return cache_file.read().strip()


def debug_print_grid(grid):
    if DEBUG:
        for line in grid:
            print(*line)
        print()


def pipe(first, *args):
    for func in args:
        first = func(first)
    return first


def benchmark(part):
    start_time = time.time()
    ans = part()
    end_time = time.time()
    print(ans, "in", end_time - start_time, "seconds")
