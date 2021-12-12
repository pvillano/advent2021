from utils import debug_print, debug_print_grid, flatten, get_day, pipe
from math import sqrt
from itertools import accumulate, count, product
from collections import defaultdict, deque
import time

test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

lines = get_day(12, test).split("\n")


def part1():
    adjacency = defaultdict(set)
    for line in lines:
        l, r = line.split("-")
        adjacency[l].add(r)
        adjacency[r].add(l)
    adjacency = {k: tuple(sorted(v)) for k, v in adjacency.items()}

    def big(c):
        return "A" <= c[0] <= "Z"

    def rec(node, seen_stack=None):
        if node == "end":
            debug_print(*seen_stack, "end")
            return 1
        if seen_stack is None:
            seen_stack = []
        tot = 0
        next_stack = seen_stack + [node]
        for nxt in adjacency[node]:
            # if seen_stack and nxt == seen_stack[-1]:
            #     continue
            if (not big(nxt)) and nxt in seen_stack:
                continue
            tot += rec(nxt, next_stack)
        return tot

    return rec("start")


def part2():
    adjacency = defaultdict(set)
    for line in lines:
        l, r = line.split("-")
        adjacency[l].add(r)
        adjacency[r].add(l)
    adjacency = {k: tuple(sorted(v)) for k, v in adjacency.items()}

    def big(c):
        return "A" <= c[0] <= "Z"

    def rec(node, seen_stack=None, vsc2=False):
        debug_print(seen_stack)
        if node == "end":
            debug_print(*seen_stack, "end")
            return 1
        if seen_stack is None:
            seen_stack = []
        tot = 0
        next_stack = seen_stack + [node]
        for nxt in adjacency[node]:
            if nxt == "start":
                continue
            if (not big(nxt)) and (nxt in seen_stack):
                if not vsc2:
                    tot += rec(nxt, next_stack, True)
                continue
            tot += rec(nxt, next_stack, vsc2)
        return tot

    return rec("start")


#
start_time = time.time()
ans = part1()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")

start_time = time.time()
ans = part2()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")
