from functools import cache
from itertools import count, product, cycle

from utils import benchmark, get_day

test = """Player 1 starting position: 4
Player 2 starting position: 8"""

lines = get_day(21, test).split("\n")
player1pos, player2pos = [int(x[-1:]) for x in lines]


def part1():
    p1idx = player1pos - 1
    p2idx = player2pos - 1
    p1score = 0
    p2score = 0
    die = cycle(range(1, 101))
    for rounds in count():
        p1idx = (p1idx + next(die) + next(die) + next(die)) % 10
        p1score += p1idx + 1
        if p1score >= 1000:
            return p2score * (rounds * 6 + 3)
        p2idx = (p2idx + next(die) + next(die) + next(die)) % 10
        p2score += p2idx + 1
        if p2score >= 1000:
            return p1score * (rounds * 6 + 6)


@cache
def my_wins(my_turn: bool, playing_pos: int, waiting_pos: int, playing_score: int = 0, waiting_score: int = 0):
    total = 0
    for roll in map(sum, product((1, 2, 3), repeat=3)):
        after_turn_pos = (playing_pos - 1 + roll) % 10 + 1
        after_turn_score = playing_score + after_turn_pos
        if after_turn_score >= 21:
            if my_turn:
                total += 1
        else:
            total += my_wins(not my_turn, waiting_pos, after_turn_pos, waiting_score, after_turn_score)
    return total


def part2():
    return max(
        my_wins(True, player1pos, player2pos), my_wins(False, player1pos, player2pos)
    )


benchmark(part1)
benchmark(part2)
