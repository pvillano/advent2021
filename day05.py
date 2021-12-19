from collections import Counter

from utils import benchmark, get_day

test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

lines = get_day(5, test).split("\n")

data = tuple(
    tuple(tuple(int(x) for x in pair.split(",")) for pair in line.split(" -> "))
    for line in lines
)


def part1():
    my_data = tuple(
        ((x1, y1), (x2, y2)) for (x1, y1), (x2, y2) in data if y1 == y2 or x1 == x2
    )
    overlaps = Counter()
    for (x1, y1), (x2, y2) in my_data:
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                overlaps[x, y] += 1
    return sum(1 for v in overlaps.values() if v > 1)


def part2():
    my_data = data
    overlaps = Counter()
    for (x1, y1), (x2, y2) in my_data:
        if x1 == x2 or y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    overlaps[x, y] += 1
        else:
            if x2 < x1:
                (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
            if len(range(x1, x2 + 1)) == 0:
                raise Exception()
            for x in range(x1, x2 + 1):
                if y2 - y1 > 0:
                    y = y1 + (x - x1)
                else:
                    y = y1 - (x - x1)
                overlaps[x, y] += 1
    return sum(1 for v in overlaps.values() if v > 1)


benchmark(part1)
benchmark(part2)
