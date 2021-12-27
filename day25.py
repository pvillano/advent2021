from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe, debug_print_grid

test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

lines = tuple(get_day(25, test).split("\n"))
height = len(lines)
width = len(lines[0])


def march(cukes: tuple[str]) -> tuple[str]:
    tmp = []
    for i in range(height):
        row = []
        for j in range(width):
            # looping happens to work with [-1]
            left, me, right = cukes[i][j - 1], cukes[i][j], cukes[i][(j + 1) % width]
            if left == ">" and me == ".":
                row.append(">")
            elif me == ">" and right == ".":
                row.append(".")
            else:
                row.append(me)
        tmp.append(row)

    ret = []
    for i in range(height):
        row = []
        for j in range(width):
            # looping happens to work with [-1]
            top, me, bot = tmp[i - 1][j], tmp[i][j], tmp[(i + 1) % height][j]
            if top == "v" and me == ".":
                row.append("v")
            elif me == "v" and bot == ".":
                row.append(".")
            else:
                row.append(me)
        ret.append("".join(row))
    return tuple(ret)


def part1():
    board = lines
    debug_print("Initial state:")
    debug_print_grid(board)
    for i in count(1):
        past = board
        board = march(board)
        debug_print(f"\nAfter {i} step{'s' if i > 1 else ''}:")
        debug_print_grid(board)
        if past == board:
            break
    return i


def part2():
    pass


benchmark(part1)
benchmark(part2)
