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


def part2():
    # rip quadratic

    # minimizing y=axx + bx + c
    # cost(x,pos) = (x-pos)*(x-pos+1)/2
    # = 1/2 * ( xx + (-2pos + 1)x +pos(pos-1)
    # min at der = 0
    # -b/2a

    data = pipe(map(int, line.split(",")), sorted, tuple)
    a = len(data) / 2
    b = sum([-2 * pos - 1 for pos in data]) / 2
    c = sum([pos * (pos - 1) for pos in data]) / 2
    debug_print(a, b, c)
    x = -b / 2 / a
    cost = a * x * x + b * x + c
    return x, cost


print(part1())
print(part2())
