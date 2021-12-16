from math import inf

from utils import benchmark, debug_print, get_day, debug_print_grid

test = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

lines = get_day(15, test).split("\n")


def part1():
    data = [tuple(map(int, x)) for x in lines]
    height = len(data)
    width = len(data[0])
    debug_print_grid(data)

    bound = 9 * (width + height)
    minprice = {(0, 0): 0}

    for y in range(height):
        for x in range(width):
            if x == y == 0:
                continue
            price = inf
            if x - 1 >= 0:
                price = min(price, minprice[(x - 1, y)] + data[y][x])
            if y - 1 >= 0:
                price = min(price, minprice[(x, y - 1)] + data[y][x])
            minprice[(x, y)] = price

    def neighbours(x, y):
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            xx = x + dx
            yy = y + dy
            if xx in range(width) and yy in range(height):
                yield xx, yy

    updated = set([(x, y) for x in range(width) for y in range(height)])
    while updated:
        nextupdated = []
        for x, y in updated:
            meprice = minprice[(x, y)]
            for xx, yy in neighbours(x, y):
                best = minprice[(xx, yy)]
                better = meprice + data[yy][xx]
                if better < best:
                    minprice[(xx, yy)] = better
                    nextupdated.append((xx, yy))
        updated = set(nextupdated)
    return minprice[(width - 1, height - 1)]


def part2():
    data = [tuple(map(int, x)) for x in lines]
    height = len(data)
    width = len(data[0])
    trueheight = height * 5
    truewidth = width * 5

    def truedata(x, y):
        xdelta, xrem = divmod(x, width)
        ydelta, yrem = divmod(y, height)
        base = data[yrem][xrem] + xdelta + ydelta
        return (base - 1) % 9 + 1

    minprice = {(0, 0): 0}

    for y in range(height * 5):
        for x in range(width * 5):
            if x == y == 0:
                continue
            price = inf
            if x - 1 >= 0:
                price = min(price, minprice[(x - 1, y)] + truedata(x, y))
            if y - 1 >= 0:
                price = min(price, minprice[(x, y - 1)] + truedata(x, y))
            minprice[(x, y)] = price

    debug_print(minprice[(truewidth - 1, trueheight - 1)])

    def neighbours(x, y):
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            xx = x + dx
            yy = y + dy
            if xx in range(width * 5) and yy in range(height * 5):
                yield xx, yy

    updated = set([(x, y) for x in range(width * 5) for y in range(height * 5)])
    while updated:
        nextupdated = []
        for x, y in updated:
            meprice = minprice[(x, y)]
            for xx, yy in neighbours(x, y):
                best = minprice[(xx, yy)]
                better = meprice + truedata(xx, yy)
                if better < best:
                    minprice[(xx, yy)] = better
                    nextupdated.append((xx, yy))
        updated = set(nextupdated)
    return minprice[(width * 5 - 1, height * 5 - 1)]


benchmark(part1)
benchmark(part2)
