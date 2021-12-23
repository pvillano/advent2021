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

test = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

lines = get_day(22, test).split("\n")


def parse_lines(lines=lines):
    def gen():
        for line in lines:
            cmd_s, coords = line.split(' ')
            cmd = cmd_s == "on"
            str_s = coords.split(',')
            pairs = tuple(tuple(int(a) for a in coord[2:].split('..')) for coord in str_s)
            yield cmd, pairs

    return tuple(gen())


def part1() -> int:
    """
        So here's some thoughts
        lets do a naive sparse grid
        x0 = max(xx[0], -50)
        x1 = min(xx[1]+1, 50+1)
    """
    data = parse_lines()
    reactor: set[tuple[int, int, int]] = set()
    for cmd, ((x0, x1), (y0, y1), (z0, z1)) in otqdm(data):
        for x in range(max(x0, -50), min(x1 + 1, 51)):
            for y in range(max(y0, -50), min(y1 + 1, 51)):
                for z in range(max(z0, -50), min(z1 + 1, 51)):
                    if cmd:
                        reactor.add((x, y, z))
                    else:
                        reactor.discard((x, y, z))
    return len(reactor)


def part2() -> int:
    """
        So here's some thoughts
        no more naive grid
        we could fragment cuboids when they intersected

        I like the idea of having doubly linked data structures from one sorting to another

        The obvious way to do this is to build a list of cuboids

        you could run from left to right,

        there's only 420 inputs (nice)
        intersection of cubes is really easy

        we just build a list of cubes and a list of negative cubes
        an intersection creates a negative cube
        a subtraction creates a negative cube

        off+x=off
        on+off = 1pos 1neg
        on+on = 2pos 1neg

        on+pos= on+neg
        on+neg = pos

        All negatives represent an area of intersection?
    """


if __name__ == '__main__':
    benchmark(part1)
    benchmark(part2)
