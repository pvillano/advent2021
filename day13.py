import time

from utils import debug_print, get_day

test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
# 7 means after 7
coords, folds = get_day(13, test).split("\n\n")
coords = [tuple(map(int, x.split(","))) for x in coords.split("\n")]
folds = folds.split("\n")
# debug_print(coords, folds)


def p1():
    mycoords = list(coords)
    for fold in folds:
        axis, coord = fold.split("=")
        axis = axis[-1]
        coord = int(coord)
        if axis == "y":
            yval = int(coord)
            newcoords = []
            for x, y in mycoords:
                if y >= yval:
                    y = yval - (y - yval)
                newcoords.append((x, y))
        elif axis == "x":
            xval = int(coord)
            newcoords = []
            for x, y in mycoords:
                if x >= xval:
                    x = xval - (x - xval)
                newcoords.append((x, y))
        else:
            raise Exception()
        mycoords = newcoords
    debug_print((sorted(set(mycoords))))
    return set(mycoords)


def part1():
    return len(p1())


def part2():
    mycoords = p1()
    width = max(x[0] for x in mycoords) + 1
    height = max(x[1] for x in mycoords) + 1
    for i in range(height):
        for j in range(width):
            if (j, i) in mycoords:
                print("[#]", end="")
            else:
                print(" . ", end="")
        print()


#
start_time = time.time()
ans = part1()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")

start_time = time.time()
ans = part2()
end_time = time.time()
print(ans, "in", end_time - start_time, "seconds")
