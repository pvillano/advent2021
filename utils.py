__all__ = [
    "benchmark",
    "DEBUG",
    "debug_print",
    "debug_print_grid",
    "debug_print_sparse_grid",
    "flatten",
    "get_day",
    "pipe",
]

import inspect
import os
import sys
import time
from itertools import chain
from typing import Any, Callable

import requests as requests

DEBUG = bool(sys.gettrace())

flatten = chain.from_iterable


def debug_print(*args, override=False, **kwargs):
    if not (DEBUG or override):
        return
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


def debug_print_grid(grid, *, override=False):
    if not (DEBUG or override):
        return
    for line in grid:
        print(*line, file=sys.stderr, flush=True)
    print()


BASE_INDENT = len(inspect.stack()) + 1


def debug_print_recursive(*args, override=False, **kwargs):
    if not (DEBUG or override):
        return
    indent = len(inspect.stack()) - BASE_INDENT
    return print(" |" * indent, *args, **kwargs, file=sys.stderr, flush=True)


def debug_print_sparse_grid(
    grid_map: dict[(int, int), Any] or set, *, transpose=False, override=False
):
    if not (DEBUG or override):
        return
    if isinstance(grid_map, set):
        grid_map = {k: "# " for k in grid_map}
    x0, x1 = min(k[0] for k in grid_map.keys()), max(k[0] for k in grid_map.keys())
    y0, y1 = min(k[1] for k in grid_map.keys()), max(k[1] for k in grid_map.keys())
    max_w = max(len(str(v)) for v in grid_map.values())
    if not transpose:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w + 1), end="", file=sys.stderr
                    )
                else:
                    print(" " * max_w, end=" ", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    else:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w + 1), end="", file=sys.stderr
                    )
                else:
                    print(" " * max_w, end=" ", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)


def pipe(first, *args: Callable):
    for func in args:
        first = func(first)
    return first


def benchmark(part: Callable):
    start_time = time.time()
    ans = part()
    end_time = time.time()
    if DEBUG:
        print(ans, "in", end_time - start_time, "seconds", file=sys.stderr)
    else:
        print(ans, "in", end_time - start_time, "seconds")


if __name__ == "__main__":

    debug_print_recursive(f"bare", override=True)

    def fib(i):
        debug_print_recursive(f"fib({i})", override=True)
        if i < 2:
            ret = 1
        else:
            ret = fib(i - 1) + fib(i - 2)
        return ret

    fib(6)
