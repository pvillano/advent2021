from collections import defaultdict
from typing import List, Set, Tuple

from utils import *
from math import *
from itertools import *

from utils import debug_print_grid

test = """2199943210
3987894921
9856789892
8767896789
9899965678"""

lines = get_day(9, test).split("\n")

board = [list(map(int, line)) for line in lines]


# debug_print(board)


def part1():
    height = len(board)
    width = len(board[0])
    score = 0
    for i, j in product(range(height), range(width)):
        is_low = True
        for di, dj in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            ii, jj = i + di, j + dj
            if ii in range(height) and jj in range(width):
                if board[i][j] >= board[ii][jj]:
                    is_low = False
        if is_low:
            debug_print(f"{i=} {j=}")
            risk_level = 1 + board[i][j]
            score += risk_level
    return score


def part2():
    height = len(board)
    width = len(board[0])

    union_find: List[List[Set[Tuple]]] = [
        [set() for j in range(width)] for i in range(height)
    ]

    for i, j in product(range(height), range(width)):
        if board[i][j] == 9:
            continue
        is_low = True
        for di, dj in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            ii, jj = i + di, j + dj
            if ii in range(height) and jj in range(width):
                if board[i][j] >= board[ii][jj]:
                    is_low = False
                if board[i][j] > board[ii][jj]:
                    union_find[i][j].add((ii, jj))
        if is_low:
            union_find[i][j] = {
                (
                    i,
                    j,
                )
            }

    debug_print_grid(union_find)

    for i, j in product(range(height), range(width)):
        cur = union_find[i][j]
        prev = None
        while cur != prev:
            prev = cur
            cur = set()
            for k in prev:
                cur.update(union_find[k[0]][k[1]])
        union_find[i][j] = cur

    debug_print_grid(union_find)

    scores = defaultdict(int)
    for row in union_find:
        for val in row:
            if len(val) == 1:
                scores[tuple(val)[0]] += 1

    rankings = sorted(list(scores.items()), key=lambda x: x[1])
    debug_print(rankings)
    return rankings[-1][1] * rankings[-2][1] * rankings[-3][1]


print(part1())
print(part2())
