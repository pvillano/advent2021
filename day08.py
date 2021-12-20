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

test = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

lines = get_day(8, test).split("\n")
data = tuple(tuple(chunk.split(" ") for chunk in line.split(" | ")) for line in lines)


def part1():
    def gen():
        for input_list, output_list in data:
            for output in output_list:
                if len(output) in (2, 4, 3, 7):
                    yield 1

    return sum(gen())


sev_to_int = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def part2():
    sum_all = 0
    for input_list, output_list in data:
        sorted_in = sorted(input_list, key=len)
        sorted_in = tuple(map(set, sorted_in))
        # number lengths 62554 56376
        # in order       23455 56667
        #                174       8
        one, seven, four, eight = (
            sorted_in[0],
            sorted_in[1],
            sorted_in[2],
            sorted_in[-1],
        )
        rest = sorted_in[3:-1]
        a = seven - one
        bd = four - one
        aeg = eight - four
        eg = aeg - a

        fivers = (x for x in rest if len(x) == 5)  # 235
        sixers = (x for x in rest if len(x) == 6)  # 069
        adg = reduce(lambda x, y: x & y, fivers)
        abfg = reduce(lambda x, y: x & y, sixers)

        b = bd & abfg
        d = bd - b
        g = adg & eg
        e = eg - g
        f = abfg - adg - b
        c = set("abcdefg") - abfg - adg - e

        # a = what wire is set to display an 'a'

        decoder = {
            a.pop(): "a",
            b.pop(): "b",
            c.pop(): "c",
            d.pop(): "d",
            e.pop(): "e",
            f.pop(): "f",
            g.pop(): "g",
        }
        num = 0
        for encoded in output_list:
            decoded = "".join(decoder[x] for x in encoded)
            decoded = "".join(sorted(decoded))
            digit = sev_to_int[decoded]
            num = num * 10 + digit
            debug_print(digit, end="")
        debug_print()
        sum_all += num
    return sum_all


benchmark(part1)
benchmark(part2)
