from collections import Counter
from copy import copy
from itertools import (
    pairwise,
)

from utils import benchmark, debug_print, get_day

test = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

first, second = get_day(14, test).split("\n\n")
template = first
rules = {x.split(" -> ")[0]: x.split(" -> ")[1] for x in second.split("\n")}

debug_print(template, rules)


def part1():
    prev = copy(template)
    for i in range(10):
        new = []
        for ab in pairwise(prev):
            new.append(ab[0])
            ab = "".join(ab)
            if ab in rules:
                new.append(rules[ab])
        new.append(prev[-1])
        prev = new
        # debug_print("".join(new))
    counter = Counter(new)
    return counter.most_common()[0][1] - counter.most_common()[-1][1]


def part2():
    pairs = Counter(["".join(ab) for ab in pairwise(template)])
    for i in range(40):
        newpairs = Counter()
        for pair, num in pairs.items():
            if pair in rules:
                a, b, c = pair[0], rules[pair], pair[1]
                newpairs["".join([a, b])] += num
                newpairs["".join([b, c])] += num
        pairs = newpairs

    c_count2 = Counter()
    for pair, num in pairs.items():
        for c in pair:
            c_count2[c] += num
    c_count2[template[0]] += 1
    c_count2[template[-1]] += 1
    c_count = Counter(**{k: v // 2 for k, v in c_count2.items()})
    debug_print(c_count.most_common())
    return (c_count2.most_common()[0][1] - c_count2.most_common()[-1][1]) // 2


benchmark(part1)
benchmark(part2)
