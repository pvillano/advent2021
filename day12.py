import time
from collections import defaultdict

from utils import debug_print, get_day

test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

lines = get_day(12, test).split("\n")


def part1():
    adjacency = defaultdict(list)
    for line in lines:
        l, r = line.split("-")
        adjacency[l].append(r)
        adjacency[r].append(l)
    adjacency = {k: tuple(sorted(v)) for k, v in adjacency.items()}

    def recurse(node, seen_stack=None):
        if node == "end":
            debug_print(*seen_stack, "end")
            return 1
        if seen_stack is None:
            seen_stack = []
        tot = 0
        next_stack = seen_stack + [node]
        for nxt in adjacency[node]:
            if nxt.isupper() or nxt not in seen_stack:
                tot += recurse(nxt, next_stack)
        return tot

    return recurse("start")


def part2():
    adjacency = defaultdict(set)
    for line in lines:
        l, r = line.split("-")
        adjacency[l].add(r)
        adjacency[r].add(l)
    adjacency = {k: tuple(sorted(v)) for k, v in adjacency.items()}

    def recurse(node, seen_stack=None, vsc2=False):
        # :param vsc2: visited small cave twice

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
            if nxt.islower() and nxt in seen_stack:
                if not vsc2:
                    tot += recurse(nxt, next_stack, True)
            else:
                tot += recurse(nxt, next_stack, vsc2)
        return tot

    return recurse("start")


#
start_time = time.time()
ans = part1()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")

start_time = time.time()
ans = part2()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")
