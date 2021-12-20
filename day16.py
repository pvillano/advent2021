import operator
from functools import reduce

from utils import benchmark, debug_print, get_day, debug_print_recursive

test = """9C0141080250320F1802104A08"""

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


def prod(items):
    running = 1
    for item in items:
        running *= item
    return running


def gt(items):
    assert len(items) == 2
    first, second = items
    if first > second:
        return 1
    return 0


def lt(items):
    return gt(items[::-1])


def eq(items):
    assert len(items) == 2
    first, second = items
    if first == second:
        return 1
    return 0


function_map = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: gt,
    6: lt,
    7: eq,
}
op_char_map = {
    0: " + ",
    1: " * ",
    2: ", ",
    3: ", ",
    5: " > ",
    6: " < ",
    7: " == ",
}


def pluck_a_packet2(remaining):
    debug_print_recursive("before", "".join(map(str, remaining)))
    version, type_id = list_to_int(remaining[0:3]), list_to_int(remaining[3:6])
    remaining = remaining[6:]
    debug_print_recursive(f"{version=} {type_id=}", end=" ")
    if type_id == 4:
        num, remaining = decode_num(remaining)
        debug_print_recursive("after", "".join(map(str, remaining)))
        return str(num), remaining
    # else
    length_type_id, *remaining = remaining
    sub_packets = []
    if length_type_id == 0:
        len_sub_packets, remaining = list_to_int(remaining[:15]), remaining[15:]
        debug_print(f"{length_type_id=} {len_sub_packets=}")
        target_length = len(remaining) - len_sub_packets
        while len(remaining) > target_length:
            packet, remaining = pluck_a_packet2(remaining)
            sub_packets.append(packet)
        if len(remaining) < target_length:
            raise Exception()
    else:
        num_sub_packets, remaining = list_to_int(remaining[:11]), remaining[11:]
        debug_print(f"{length_type_id=} {num_sub_packets=}")
        for i in range(num_sub_packets):
            packet, remaining = pluck_a_packet2(remaining)
            sub_packets.append(packet)
    op = function_map[type_id]
    debug_print_recursive("after", "".join(map(str, remaining)))

    op_char = op_char_map[type_id]
    if type_id == 2:
        ret = f"min([{op_char.join(sub_packets)}])"
    elif type_id == 3:
        ret = f"max([{op_char.join(sub_packets)}])"
    else:
        ret = f"({op_char.join(sub_packets)})"
    return ret, remaining


def part2():
    return pluck_a_packet2(data)[0]


if __name__ == "__main__":
    # benchmark(part1)
    # benchmark(part2)
    p2 = part2()
    print(f"{p2} = {eval(p2)}")
