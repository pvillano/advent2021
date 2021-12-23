from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

test = """"""

lines = get_day(23, test).split("\n")


def part1():
    """
    #############
    #...........#
    ###4#2#4#1###
      #3#3#1#2#
      #########

    #############
    #.1.........# 8
    ###4#2#4# ###
      #3#3#1#2#
      #########

    #############
    #.1.......2 # 30
    ###4#2#4# ###
      #3#3#1# #
      #########

    #############
    #.1.......2 # 13000 MIN
    ### #2# #4###
      #3#3#1#4#
      #########

    #############
    #11.......2 # 8
    ### #2# #4###
      #3#3# #4#
      #########

    #############
    #11.......2 #
    ### #2# #4### 800
      # #3#3#4#
      #########

    #############
    #  .......2 # 8
    ###1#2# #4###
      #1#3#3#4#
      #########

    #############
    #  .2.....2 # 20
    ###1# # #4###
      #1#3#3#4#
      #########


    #############
    #  .2.....2 #
    ###1# #3#4### 500 MIN
      #1# #3#4#
      #########
    #############
    #  .        # 90
    ###1#2#3#4###
      #1#2#3#4#
      #########

    """
    # not 14436
    # return (8+4+1)*1000+(5+7+1)*100+(7+4+1)*10+(7+8+1)*1
    # not 14474
    # return sum((8, 30, 13000,8,800,8,20,500,100))
    # not 14464
    return sum((8, 30, 13000,8,800,8,20,500,90))
    # return (13)*1000+(13)*100+(14)*10+(16-24)*1???
    # not 14464
    # return (13) * 1000 + (13) * 100 + (14) * 10 + (20) * 1
    # not 14480
    return 14460


def part2():
    """
    so theres 7 hallway spots
    16 room spots
    4^23=2^46=64TB

    each piece out(8) in(1)
    its still a lot


    """


benchmark(part1)
benchmark(part2)
