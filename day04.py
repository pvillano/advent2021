from utils import benchmark, debug_print, get_day

test = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

numbers_str, *boards_str_list = get_day(4, test).split("\n\n")
numbers = tuple(map(int, numbers_str.split(",")))

boards = []
for board_str in boards_str_list:
    board = []
    for line in board_str.split("\n"):
        board.append(tuple(int(x) for x in line.split(" ") if x))
    boards.append(board)
debug_print(boards)


def has_bingo(board):
    for i in range(5):
        if all(board[i][j] for j in range(5)):
            return True
        if all(board[j][i] for j in range(5)):
            return True
    # if all(board[i][i] for i in range(5)):
    #     return True
    # if all(board[i][4-i] for i in range(5)):
    #     return True
    return False


def score(board, marks, just_called):
    tot = 0
    for i in range(5):
        for j in range(5):
            if not marks[i][j]:
                tot += board[i][j]
    return tot * just_called


def part1():
    board_marks = [[[False] * 5 for j in range(5)] for i in range(len(boards))]
    for num in numbers:
        for i in range(len(boards)):
            for j in range(5):
                for k in range(5):
                    if boards[i][j][k] == num:
                        board_marks[i][j][k] = True
                        if has_bingo(board_marks[i]):
                            return score(boards[i], board_marks[i], num)


def part2():
    board_marks = [[[False] * 5 for j in range(5)] for i in range(len(boards))]
    has_won = [False] * len(boards)
    for num in numbers:
        for i in range(len(boards)):
            for j in range(5):
                for k in range(5):
                    if boards[i][j][k] == num:
                        board_marks[i][j][k] = True
                        if has_bingo(board_marks[i]):
                            has_won[i] = True
                            if sum(has_won) == len(boards):
                                loser_idx = i
                                return score(boards[i], board_marks[i], num)


benchmark(part1)
benchmark(part2)
