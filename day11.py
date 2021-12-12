from utils import *
from math import *
from itertools import *

test = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

lines = get_day(11, test).split("\n")


board = []

for line in lines:
    board.append([int(x) for x in line])
height = len(board)
width = len(board[0])

tot_flashes = 0
for k in count(1):
    # inc
    for row in board:
        for j in range(width):
            row[j] += 1
    # flash
    flashed = [[False] * width for i in range(height)]
    a_flashed = True
    while a_flashed:
        a_flashed = False
        for i in range(height):
            for j in range(width):
                if board[i][j] > 9 and not flashed[i][j]:
                    a_flashed = True
                    flashed[i][j] = True
                    tot_flashes += 1
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if i + di >= 0 and j + dj >= 0:
                                try:
                                    board[i + di][j + dj] += 1
                                except IndexError:
                                    pass
                    board[i][j] -= 1

    for i in range(height):
        for j in range(width):
            if board[i][j] > 9:
                board[i][j] = 0
    print(f"{k=}")
    for row in board:
        print(*row)
    if not any(map(any, board)):
        print(k)
        exit()
