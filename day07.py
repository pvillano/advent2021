from functools import partial

from utils import *
from math import *
from itertools import *

test = """16,1,2,0,4,2,7,1,2,14"""

line = get_day(7, test)


def part1():
    # to minimize cost, traverse the list until
    # cost of a spot is sum(here-left) + sum (right-here)#
    data = pipe(map(int, line.split(",")), sorted, tuple)
    debug_print(data)
    sum_left = tuple(accumulate(data))
    debug_print(sum_left)
    sum_right = pipe(
        data, reversed, accumulate, tuple, reversed, tuple  # defaults to sum
    )
    debug_print(sum_right)

    def it():
        for i, l, x, r in zip(range(len(data)), sum_left, data, sum_right):
            cost = ((i + 1) * x - l) + (r - (len(data) - i) * x)
            yield cost, x

    return min(it())[0]


def triangle(k):
    # 0,1,3,6,10
    k = abs(k)
    return (k * (k + 1)) // 2


def cost(data, x):
    return sum(triangle(k - x) for k in data)


def part2():
    data = pipe(map(int, line.split(",")), sorted, tuple)
    return min(cost(data, x) for x in range(min(data), max(data)))


print(part1())
print(part2())
