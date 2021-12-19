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

from utils import benchmark, debug_print, get_day, pipe

test = """3,4,3,1,2"""

fish_list = [int(fish) for fish in get_day(6, test).split(",")]
initial_fish = Counter(fish_list)


def part1():
    fish = Counter(initial_fish)
    for i in range(80):
        fish = Counter({(k - 1): v for k, v in fish.items()})
        spawn_count = fish.pop(-1, 0)
        fish[6] += spawn_count
        fish[8] += spawn_count
    return sum(fish.values())


def part2():
    fish = Counter(initial_fish)
    for i in range(256):
        fish = Counter({(k - 1): v for k, v in fish.items()})
        spawn_count = fish.pop(-1, 0)
        fish[6] += spawn_count
        fish[8] += spawn_count
    return sum(fish.values())


benchmark(part1)
benchmark(part2)
