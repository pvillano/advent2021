from collections import defaultdict
from itertools import count
from math import inf

from utils import debug_print, get_day, flatten

test = """target area: x=20..30, y=-10..-5"""

line = get_day(17, test)
line = line.lstrip("target area: x=")
xx, yy = line.split(", y=")
x1, x2 = map(int, xx.split(".."))
y1, y2 = map(int, yy.split(".."))
debug_print(f"{x1=} {x2=} {y1=} {y2=} ")


def part1():
    # vx0ts = defaultdict(list)
    t_set = set()
    min_t_stop = inf
    for vx0 in range(1, x2 + 1):
        vx00 = vx0
        x = 0
        t = 0
        while x <= x2:
            if x >= x1:
                # vx0ts[vx0].append(t)
                debug_print(f"{vx00=} {t=} {x=}")
                t_set.add(t)
            x += vx0
            vx0 -= 1
            t += 1
            if vx0 == 0:
                if x >= x1:
                    debug_print(f"STOP {vx00=} {t=} {x=}")
                    min_t_stop = min(min_t_stop, t)
                break
    debug_print(f"{min_t_stop=}")
    debug_print(f"{t_set=}")
    best = -inf
    t_short = sorted(t for t in t_set if t < min_t_stop)

    def t_gen():
        yield from t_short
        yield from count(min_t_stop)

    y0_list = []
    valid_highest = 0
    for y0 in count():
        highest = 0
        for t in t_gen():
            y = t * (y0 + y0 - t + 1) / 2
            highest = max(y, highest)
            if y >= y1:
                if y <= y2:
                    y0_list.append(y0)
                    valid_highest = max(valid_highest, highest)
                    print(f"{valid_highest=}")
            else:
                break

    return valid_highest
    # for t in t_set:
    #     # solve for y0
    #     # y= 0 t=0
    #     # y = y0 t=1
    #     # y= y0 y0-1 t=2
    #     # y = t*(y0 + y0 - t + 1)/2
    #     # 2y/t = y0 + y0 - t + 1
    #     # y0 = (2y/t+t-1)/2
    #     y01 = (2 * y1 / t + t - 1) / 2
    #     y02 = (2 * y2 / t + t - 1) / 2
    #     for y0 in range(int(ceil(y01)), int(floor(y02))+1):
    #         y = t*(y0 + y0 - t + 1) / 2
    #         if y in range(y1, y2+1):
    #             for i in range(t+1):
    #                 yyy = i*(y0 + y0 - t + 1) / 2
    #                 if yyy > best:
    #                     best = yyy
    return best


def part2():
    # vx0ts = defaultdict(list)
    t_set = set()
    min_t_stop = inf
    t_stop_list = []
    t_to_v0_count_dict = defaultdict(int)
    xv0_set = set()
    for vx0 in range(1, x2 + 1):
        vx00 = vx0
        x = 0
        t = 0
        while x <= x2:
            if x >= x1:
                # vx0ts[vx0].append(t)
                debug_print(f"{vx00=} {t=} {x=}")
                t_set.add(t)
                t_to_v0_count_dict[t] += 1
                xv0_set.add(vx00)
            x += vx0
            vx0 -= 1
            t += 1
            if vx0 == 0:
                if x >= x1:
                    debug_print(f"STOP {vx00=} {t=} {x=}")
                    min_t_stop = min(min_t_stop, t)
                    t_stop_list.append(t)
                break
    debug_print(f"{min_t_stop=}")
    debug_print(f"{t_set=}")
    t_short = sorted(t for t in t_set if t < min_t_stop)

    def t_gen():
        yield from t_short
        yield from count(min_t_stop)

    def t_to_v0_count_fun(t):
        base_count = t_to_v0_count_dict[t]
        # return base_count + sum(1 for tt in t_stop_list if t>tt)
        return base_count + sum(1 for tt in t_stop_list if t > tt)

    v0y0_set = set()
    for y0 in flatten(zip(count(), count(step=-1))):
        highest = 0
        for t in t_gen():
            y = t * (y0 + y0 - t + 1) / 2
            if y >= y1:
                if y <= y2:
                    for xv0 in xv0_set:
                        x = t * (xv0 + xv0 - t + 1) / 2
                        backwards_motion = t > xv0 + 1
                        if not backwards_motion and x in range(x1, x2 + 1):
                            v0y0_set.add((xv0, y0))
                            debug_print(len(v0y0_set))
            else:
                break
    return


def part2silly():
    total = 0
    for radius in count():
        for y0 in range(-radius, radius + 1):
            x0 = radius - abs(y0)
            xv, yv = x0, y0
            x, y = 0, 0
            for t in count():
                x += xv
                y += yv
                xv -= 1 if xv > 0 else 0
                yv -= 1
                if x in range(x1, x2 + 1) and y in range(y1, y2 + 1):
                    total += 1
                    print(f"{total=} {x0=} {y0=}")
                    break
                if x > x2 or y < y1:
                    break


def day17(txt="""target area: x=20..30, y=-10..-5"""):
    (x_min, x_max), (y_min, y_max) = [
        map(int, a[2:].split("..")) for a in txt[13:].split(", ")
    ]
    total, highest = 0, 0
    for radius in count():
        for yv in range(-radius, radius + 1):
            xv = radius - abs(yv)
            x, y = 0, 0
            h_candidate = 0
            while x <= x_max and y >= y_min:
                if x >= x_min and y <= y_max:
                    total += 1
                    highest = max(highest, h_candidate)
                    print(f"{highest=} {total=}")
                    break
                x += xv
                y += yv
                xv -= 1 if xv > 0 else 0
                yv -= 1
                h_candidate = max(y, h_candidate)


# benchmark(part1)
# benchmark(part2)
