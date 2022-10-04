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

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

test = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
lines = get_day(23, test).split("\n")

test_rooms = tuple(tuple(ord(lines[r][c]) - ord('A') for r in reversed(range(2, len(lines) - 1))) for c in (3, 5, 7, 9))

test_hallway = (None,) * 7


def cost_to_finish_p1(hallway: str, rooms: tuple[str, str, str, str]):
    if rooms == tuple((x, x) for x in range(4)):
        return 0
    # for option in []:
    #     cost_of_option = compute_distance(a,b) * (1**amphipod_type)
    #     cost_of_rest = cost_to_finish(new_hallway, new_rooms)
    #     if cost_of_rest is not None:
    #         yield cost_of_option + cost_of_rest

    # first priority: move from hallway to room


def distance_p1(column1=None, height1=None, hallway_idx=None, column2=None, height2=None):
    hallway_x_map = [1, 2, 4, 6, 8, 10, 11]
    if hallway_idx is not None:
        dx = abs((2 + column1 * 2) - hallway_x_map[hallway_idx])
        dy = 2 - height1
        return dx + dy
    if


def part1() -> int:
    hallway = "......."
    rooms = ("BA", "CD", "BC", "DA")


def part2() -> int:
    return 0


if __name__ == '__main__':
    benchmark(part1)
    benchmark(part2)
