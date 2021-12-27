from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    pairwise,
)

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

lines = get_day(24, "", override=True).split("\n")

chunks = [lines[i * 18:i * 18 + 18] for i in range(14)]


def invariants():
    for chunk in chunks:
        assert len(chunk) == 18
        assert chunk[0:4] == lines[0:4]
        # line 4 is const0
        assert chunk[4] in ["div z 1", "div z 26"]
        # line 5 is const1
        assert chunk[6:15] == lines[6:15]
        # line 15 is const2
        assert chunk[16:18] == lines[16:18]


def apply_round(w, z, c0, c1, c2):
    assert c0 in (1, 26)
    if w == ((z % 26) + c1):
        return z//c0
    else:
        return z//c0 * 26 + w + c2


# benchmark(part1)
# benchmark(part2)

invariants()
line_by_line = """
input w
x = 0
x = z
mod x 26

div z 26 or div z 1

add x CONSTANT

eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w

add y CONSTANT

mul y x
add z y
"""

shortened1 = """
input w
x = z mod 26 + CONSTANT

div z 26 or div z 1

x = x != w
y = 25 * x + 1
z = z*y
y = w + CONSTANT

z = z + y * x
"""

shortened2 = """
input w
x = ((z mod 26) + c1) != w
z2 //= 26 or //= 1
z3 = z2*(25*x + 1)+(w + c2) * x
"""

"""

c1 can be negative
c2 is always positive

for z3 to be zero
    if z was zero
        only if x= 0
            i.e. w=(z mod 26 + c1)
            i.e. w = c1 NEVER
    else z is positive
        pass
    if x = 0 i.e. w=(z mod 26 + c1)
        only if z2=0
            if z = 0
            OR
            if c0=26 and z<26
    else x = 1 i.e. w!=(z mod 26 + c1)
        if 0 = z2*26+w+c2
        only if z<0
        


"""
