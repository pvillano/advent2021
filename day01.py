from itertools import count

from utils import *

lines = get_day(1, 2021).strip().split("\n")
nums = list(map(int, lines))
#################################################
s = 0
for a, b in zip(nums, nums[1:]):
    if a < b:
        s += 1
print(s)
#################################################
s = 0
try:
    for i in count():
        if sum(nums[i : i + 3]) < sum(nums[i + 1 : i + 4]):
            s += 1
finally:
    print(s)
