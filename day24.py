from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    pairwise,
)

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

lines = get_day(24, "", override=True).split("\n")

chunks = [lines[i * 18:i * 18 + 18] for i in range(14)]


def invariants():
    for chunk in chunks:
        assert len(chunk) == 18
        assert chunk[0:4] == lines[0:4]

        c0 = int(chunk[4].split(" ")[-1])
        assert c0 in (1, 26)

        c1 = int(chunk[5].split(" ")[-1])
        assert c1 not in range(1, 10)
        assert chunk[6:15] == lines[6:15]

        c2 = int(chunk[15].split(" ")[-1])
        assert c2 > 0
        assert chunk[16:18] == lines[16:18]
        yield c0, c1, c2


def apply_round(w, z, c0, c1, c2):
    assert 0 < w < 10
    assert c0 in (1, 26)
    assert c1 not in range(0, 10)
    assert c2 > 0
    assert z >= 0
    if w == ((z % 26) + c1):
        return z // c0
    else:
        return z // c0 * 26 + w + c2  # never 0


def part0():
    constant_list = tuple(invariants())
    acceptable_zw = defaultdict(set)
    acceptable_zw[14] = {(0, None)}

    max_z_in_list = []
    max_z_in = 0
    for step in range(14):
        max_z_in_list.append(max_z_in)
        c0, c1, c2 = constant_list[step]
        max_z_in = max_z_in // c0 * 26 + 9 + c2

    max_z_in_list = [999] * 14
    for step in reversed(range(14)):
        c0, c1, c2 = constant_list[step]
        acceptable_output_z = [x[0] for x in acceptable_zw[step + 1]]

        if c1 > 9:
            # return z // c0 * 26 + w + c2
            for w in range(1, 10):
                for output_z in acceptable_output_z:
                    z_over_c0 = output_z - w - c2
                    if z_over_c0 < 0:
                        continue
                    for in_z in range(c0 * z_over_c0, c0 * (z_over_c0 + 1)):
                        if in_z > max_z_in_list[step]:
                            break
                        acceptable_zw[step].add((in_z, w))
        else:
            assert c1 < 0
            # top branch
            for w in range(1, 10):
                z_mod = w - c1
                if z_mod >= 26:
                    continue
                in_z = z_mod
                while in_z // c0 <= max(acceptable_output_z):
                    if in_z > max_z_in_list[step]:
                        break
                    acceptable_zw[step].add((in_z, w))
                    in_z += 26
            # bottom branch
            for w in range(1, 10):
                for output_z in acceptable_output_z:
                    z_over_c0 = output_z - w - c2
                    if z_over_c0 < 0:
                        continue
                    for in_z in range(c0 * z_over_c0, c0 * (z_over_c0 + 1)):
                        if in_z > max_z_in_list[step]:
                            break
                        acceptable_zw[step].add((in_z, w))
        # debug_print(step, acceptable_zw[step])
        debug_print(step, len(acceptable_zw[step]))


def part1():
    constant_list = tuple(invariants())

    @cache
    def first_working_w(z=0, step=0):
        c0, c1, c2 = constant_list[step]
        if step == 13:
            for w in reversed(range(1, 10)):
                z_out = apply_round(w, z, c0, c1, c2)
                if z_out == 0:
                    return [w]
            return None
        for w in reversed(range(1, 10)):
            z_out = apply_round(w, z, c0, c1, c2)
            w_chain = first_working_w(z_out, step + 1)
            if w_chain is not None:
                return [w] + w_chain

    return int("".join([str(x) for x in first_working_w()]))


if __name__ == '__main__':
    benchmark(part1)
