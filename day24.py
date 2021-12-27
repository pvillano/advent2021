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

test = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

lines = get_day(24, test, override=True).split("\n")


def part0():
    registers = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }
    for line in lines:

        instr, a, *_ = line.split()
        if instr == "inp":
            registers[a] = int(input(a))  # lol
        else:
            var_s = line.split(" ")[2]
            if var_s in "wxyz":
                b = registers[var_s]
            else:
                b = int(var_s)

            if instr == "add":
                registers[a] = registers[a] + b
            elif instr == "mul":
                registers[a] = registers[a] * b
            elif instr == "div":
                registers[a] = registers[a] // b
            elif instr == "mod":
                registers[a] = registers[a] % b
            elif instr == "eql":
                registers[a] = int(registers[a] == b)
            else:
                assert False
        debug_print(registers)


def part1():
    registers = {
        "w": deque(["0"]),
        "x": deque(["0"]),
        "y": deque(["0"]),
        "z": deque(["0"]),
    }
    inputcount = 0
    for line in otqdm(lines):

        instr, a, *_ = line.split()
        if instr == "inp":
            registers[a] = deque([f"in_list[{inputcount}]"])
            inputcount += 1
        else:
            var_s = line.split(" ")[2]
            if var_s in "wxyz":
                b = registers[var_s]
            else:
                b = var_s

            new = deque()
            new.append("(")
            new.append(registers[a])
            if instr == "add":
                new.append(" + ")
            elif instr == "mul":
                new.append(" * ")
            elif instr == "div":
                new.append(" // ")
            elif instr == "mod":
                new.append(" % ")
            elif instr == "eql":
                new.append(" == ")
            else:
                assert False
            new.append(b)
            new.append(")")
            registers[a] = new
        # debug_print(registers)
    with open("out.py", "w") as f:
        for s in rec_print(registers["z"]):
            f.write(s)


def rec_print(remaining):
    # for i in count():
    #     if not remaining:
    #         break
    while remaining:
        cur = remaining.popleft()
        if cur is remaining:
            pass
        if isinstance(cur, str):
            yield cur
        elif len(cur) > 0:
            cur2 = cur.popleft()
            if len(cur) > 0:
                remaining.appendleft(cur)
            remaining.appendleft(cur2)


def part2():
    pass


# benchmark(part1)
# benchmark(part2)
