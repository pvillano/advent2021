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

test = """Player 1 starting position: 4
Player 2 starting position: 8"""

lines = get_day(21, test).split("\n")
player1pos, player2pos = [int(x[-1:]) for x in lines]


def die():
    while True:
        for i in range(1, 101):
            yield i


def part1():
    p1idx = player1pos - 1
    p2idx = player2pos - 1
    p1score = 0
    p2score = 0
    iter = enumerate(die(), 1)
    rolls = 0
    while True:
        # for i in range(5):
        (_, r1), (_, r2), (rolls, r3) = next(iter), next(iter), next(iter)
        p1idx = (p1idx + r1 + r2 + r3) % 10
        p1score += p1idx + 1
        # debug_print(f"1: {r1, r2, r3=} {p1idx+1=} {p1score=}")
        if p1score >= 1000:
            return p2score * rolls
        (_, r1), (_, r2), (rolls, r3) = next(iter), next(iter), next(iter)
        p2idx = (p2idx + r1 + r2 + r3) % 10
        p2score += p2idx + 1
        # debug_print(f"1: {r1, r2, r3=} {p2idx+1=} {p2score=}")
        if p2score >= 21:
            return p1score * rolls


@cache
def p1wins(first, second, first_score, second_score):
    tot_wins = 0
    for i, j, k in product(*[[1, 2, 3]] * 3):
        new_p1pos = (first + i + j + k) % 10
        new_p1score = first_score + new_p1pos + 1
        if new_p1score >= 21:
            tot_wins += 1
        else:
            tot_wins += p2wins(second, new_p1pos, second_score, new_p1score)
    return tot_wins


@cache
def p2wins(first_idx, second_idx, first_score, second_score):
    tot_wins = 0
    for i, j, k in product((1, 2, 3), (1, 2, 3), (1, 2, 3)):
        new_p1pos = (first_idx + i + j + k) % 10
        new_p1score = first_score + new_p1pos + 1
        if new_p1score >= 21:
            tot_wins += 0
        else:
            tot_wins += p1wins(second_idx, new_p1pos, second_score, new_p1score)
    return tot_wins


def part2():
    p1idx = player1pos - 1
    p2idx = player2pos - 1
    return max(p1wins(p1idx, p2idx, 0, 0), p2wins(p1idx, p2idx, 0, 0))


benchmark(part1)
benchmark(part2)
