import operator
from functools import reduce

from utils import benchmark, debug_print, get_day, debug_print_recursive

test = """A0016C880162017C3686B18A3D4780"""

line = get_day(16, test, override=True)
data_long = int(line, 16)
data_str = format(data_long, "b").rjust(len(line) * 4, "0")
data: tuple[int] = tuple(int(x) for x in data_str)


def list_to_int(l):
    as_str = "".join(str(x) for x in l)
    return int(as_str, 2)


def decode_num(remaining):
    num = 0
    while remaining[0] == 1:
        _, *int_bits = remaining[:5]
        remaining = remaining[5:]
        num = (num << 4) + list_to_int(int_bits)
    _, *int_bits = remaining[:5]
    remaining = remaining[5:]
    num = (num << 4) + list_to_int(int_bits)
    debug_print(f"{num=}")
    return num, remaining


def pluck_a_packet(remaining):
    debug_print_recursive("before", "".join(map(str, remaining)))
    version, type_id = list_to_int(remaining[0:3]), list_to_int(remaining[3:6])
    remaining = remaining[6:]
    debug_print_recursive(f"{version=} {type_id=}", end=" ")
    if type_id == 4:
        num, remaining = decode_num(remaining)
        # return num, remaining
        return version, remaining
    else:
        length_type_id, *remaining = remaining
        sub_packets = []
        if length_type_id == 0:
            len_sub_packets, remaining = list_to_int(remaining[:15]), remaining[15:]
            debug_print(f"{length_type_id=} {len_sub_packets=}")
            target_length = len(remaining) - len_sub_packets
            while len(remaining) > target_length:
                packet, remaining = pluck_a_packet(remaining)
                sub_packets.append(packet)
            if len(remaining) < target_length:
                raise Exception()
        else:
            num_sub_packets, remaining = list_to_int(remaining[:11]), remaining[11:]
            debug_print(f"{length_type_id=} {num_sub_packets=}")
            for i in range(num_sub_packets):
                packet, remaining = pluck_a_packet(remaining)
                sub_packets.append(packet)
    debug_print_recursive("after", "".join(map(str, remaining)))
    return version + sum(sub_packets), remaining


def part1():
    return pluck_a_packet(list(data))[0]


def part2():
    pass


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
