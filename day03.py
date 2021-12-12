from collections import defaultdict

from utils import *

lines = get_day(3).split("\n")


# lines = """00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010""".split('\n')
########################################

d = defaultdict(int)
for line in lines:
    for i, bit in enumerate(line):
        if bit == "1":
            d[i] += 1
        else:
            d[i] -= 1

gam = ""
eps = ""
for i, cnt in sorted(list(d.items())):
    if cnt > 0:
        gam += "1"
        eps += "0"
    else:
        gam += "0"
        eps += "1"
val = int(gam, 2) * int(eps, 2)
print(val)
##################################

ogr = 0
sr = 0


def mcv(l, idx):
    d2 = defaultdict(int)
    for bitstring in l:
        d2[bitstring[idx]] += 1
    if d2["0"] > d2["1"]:
        return "0"
    else:
        return "1"


def lcv(l, idx):
    d2 = defaultdict(int)
    for s in l:
        d2[s[idx]] += 1
    if d2["0"] <= d2["1"]:
        return "0"
    else:
        return "1"


newlines = lines.copy()
for i in range(len(lines[0])):
    debug_print(i, newlines)
    mc = mcv(newlines, i)
    debug_print(i, newlines)
    newlines = [x for x in newlines if x[i] == mc]

debug_print(newlines)
ogr = int(newlines[0], 2)

newlines = lines.copy()
for i in range(len(lines[0])):
    if len(newlines) == 1:
        break
    mc = lcv(newlines, i)
    newlines = [x for x in newlines if x[i] == mc]

debug_print(newlines)
sr = int(newlines[0], 2)
print(ogr * sr)
