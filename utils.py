__all__ = [
    "benchmark",
    "DEBUG",
    "debug_print",
    "debug_print_grid",
    "flatten",
    "get_day",
    "pipe",
]

import inspect
import os
import sys
import time
from itertools import chain
from typing import Any

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


BASE_INDENT = len(inspect.stack()) + 1


def debug_print_recursive(*args, **kwargs):
    if DEBUG:
        indent = len(inspect.stack())
        return print("| " * indent, *args, **kwargs, file=sys.stderr, flush=True)


def debug_print_sparse_grid(grid_map: dict[(int, int), Any], override=False):
    if not (DEBUG or override):
        return
    x0, x1 = min(k[0] for k in grid_map.keys()), max(k[0] for k in grid_map.keys())
    y0, y1 = min(k[1] for k in grid_map.keys()), max(k[1] for k in grid_map.keys())
    max_w = max(len(str(v)) for v in grid_map.values())
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x, y) in grid_map:
                print(str(grid_map[(x, y)]).rjust(max_w + 1), end="")
            else:
                print(" " * max_w, end=" ")
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


if __name__ == '__main__':
    def fib(i):
        debug_print_recursive(f"fib({i})")
        if i < 2:
            ret = 1
        else:
            ret = fib(i - 1) + fib(i - 2)
        return ret

    fib(6)
