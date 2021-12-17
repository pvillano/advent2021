import operator
from functools import reduce

from utils import benchmark, debug_print, get_day

test = """9C0141080250320F1802104A08"""

line = get_day(16, test, override=True)
# data = (tuple(map(int, line)) for line in lines)
# data = (tuple(map(int, line.split('\n'))) for line in lines)
data = int(line, 16)
data = format(data, "b").rjust(len(line) * 4, "0")
# data = data.rstrip('0')
data = tuple(int(x) for x in data)
# debug_print(data)
data: tuple[int]


def list_int(l):
    return int("".join(map(str, l)), 2)


def part1():
    return parse1(data)


def parse1(remaining, lennn=1):
    ret = []
    for i in range(lennn):
        if not remaining:
            break
        ver, id, remaining = remaining[:3], remaining[3:6], remaining[6:]
        debug_print(f"{ver=}")
        if id == (1, 0, 0):  # literal
            debug_print("literal")
            litval = 0
            bits, remaining = remaining[:5], remaining[5:]
            debug_print(bits)
            while bits[0] == 1:
                debug_print(bits)
                litval <<= 4
                litval += list_int(bits[1:])
                bits, remaining = remaining[:5], remaining[5:]
            debug_print(bits)
            litval <<= 4
            litval += list_int(bits[1:])
            debug_print(litval)
            ret.append(litval)
        else:  # operator
            opnum = list_int(id)
            debug_print("op", opnum)
            operators = (
                operator.add,
                operator.mul,
                min,
                max,
                "literal",
                operator.gt,
                operator.lt,
                operator.eq,
            )
            length_type, remaining = remaining[0], remaining[1:]
            if length_type == 0:
                total_length_bits, remaining = remaining[:15], remaining[15:]
                lenpackets = list_int(total_length_bits)
                debug_print("substing length", lenpackets)
                sub_packet, remaining = remaining[:lenpackets], remaining[lenpackets:]
                ret.append(
                    reduce(
                        operators[opnum], parse1(sub_packet, 9999999999999999999999)[0]
                    )
                )
            else:
                numpacketsbits, remaining = remaining[:11], remaining[11:]
                numpackets = list_int(numpacketsbits)
                debug_print("count length", numpackets)

                myval, remaining = parse1(remaining, numpackets)
                ret.append(reduce(operators[opnum], myval))
    return ret, remaining


def part2():
    pass


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
