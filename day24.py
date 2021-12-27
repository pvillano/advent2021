from functools import cache

from utils import benchmark, get_day

lines = get_day(24, "", override=True).split("\n")

chunks = [lines[i * 18 : i * 18 + 18] for i in range(14)]


def extract_constants():
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
        return z // c0  # always smaller
    else:
        return z // c0 * 26 + w + c2  # never 0


def part1():
    constant_list = tuple(extract_constants())

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


uh_oh = 0


def part2():
    constant_list = tuple(extract_constants())

    max_z_in = {14: 0}

    for step in reversed(range(14)):
        c0, c1, c2 = constant_list[step]
        max_z_in[step] = max_z_in[step + 1] * c0 + c0 - 1

    max_z_out = tuple(max_z_in[x + 1] for x in range(14))

    @cache
    def first_working_w(z=0, step=0):
        global uh_oh
        c0, c1, c2 = constant_list[step]
        if step == 13:
            for w in range(1, 10):
                z_out = apply_round(w, z, c0, c1, c2)
                if z_out == 0:
                    return [w]
            return
        for w in range(1, 10):
            z_out = apply_round(w, z, c0, c1, c2)
            if z_out > max_z_out[step]:
                continue
            w_chain = first_working_w(z_out, step + 1)
            if w_chain is not None:
                return [w] + w_chain

    return int("".join(str(x) for x in first_working_w()))


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
    pass
