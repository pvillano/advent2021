from utils import *
from math import *
from itertools import *

test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

lines = get_day(10, test).split("\n")

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
#####################################
score = 0
for line in lines:
    stack = []
    for ch in line:
        if ch in "[{(<":
            stack.append(ch)
        else:
            if not stack:
                debug_print(f"{line=} {ch=}")
                score += scores[ch]
            else:
                opener = stack.pop()
                if opener + ch not in {"[]", "{}", "()", "<>"}:
                    debug_print(f"{line=} {ch=} {opener=}")
                    score += scores[ch]
print(score)


###############################


def remaining_chars(line):
    stack = []
    for ch in line:
        if ch in "[{(<":
            stack.append(ch)
        else:
            if not stack:  # malformed
                debug_print(f"{line=} {ch=}")
                return []
            else:
                opener = stack.pop()
                if opener + ch not in {"[]", "{}", "()", "<>"}:  # malformed
                    return []
    return stack


score = []
scores = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

for line in lines:
    line_score = 0
    chars = remaining_chars(line)
    for ch in reversed(chars):
        line_score *= 5
        line_score += scores[ch]
    debug_print("".join(chars), line_score)
    if line_score:
        score.append(line_score)

print(sorted(score)[len(score) // 2])
