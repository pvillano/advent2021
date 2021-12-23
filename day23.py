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

from utils import benchmark, debug_print, get_day, pipe

test = """"""

lines = get_day(23, test).split("\n")


def part1() -> int:
    """
    lol do it by hand
    """
    return 14460


def part2():
    """
    so theres 7 hallway spots
    16 room spots
    4^23=2^46=64TB

    each piece out(8) in(1)
    its still a lot


    """


benchmark(part1)
benchmark(part2)
