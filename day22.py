from otqdm import otqdm

from utils import benchmark, get_day

test = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

Cuboid = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]

lines = tuple(get_day(22, test).split("\n"))


def parse_lines(line_list=lines):
    def gen():
        for line in line_list:
            cmd_s, coords = line.split(" ")
            cmd = cmd_s == "on"
            str_s = coords.split(",")
            pairs = tuple(
                tuple(int(a) for a in coord[2:].split("..")) for coord in str_s
            )
            yield cmd, pairs

    return tuple(gen())


def part1() -> int:
    """
    So here's some thoughts
    lets do a naive sparse grid
    x0 = max(xx[0], -50)
    x1 = min(xx[1]+1, 50+1)
    """
    data = parse_lines()
    reactor: set[tuple[int, int, int]] = set()
    for cmd, ((x0, x1), (y0, y1), (z0, z1)) in otqdm(data):
        for x in range(max(x0, -50), min(x1 + 1, 51)):
            for y in range(max(y0, -50), min(y1 + 1, 51)):
                for z in range(max(z0, -50), min(z1 + 1, 51)):
                    if cmd:
                        reactor.add((x, y, z))
                    else:
                        reactor.discard((x, y, z))
    return len(reactor)


def cuboid_intersection(a: Cuboid, b: Cuboid) -> Cuboid | None:
    c = tuple((max(a0, b0), min(a1, b1)) for (a0, a1), (b0, b1) in zip(a, b))
    if any(c0 > c1 for c0, c1 in c):
        return None
    return c


def cuboid_difference(a: Cuboid, b: Cuboid) -> list[Cuboid]:
    """
    The idea is to slice off faces of `a` into separate cubes
    """
    ret: list[Cuboid] = []
    for i in range(3):
        if a[i][0] < b[i][0] <= a[i][1]:
            left = [list(x) for x in a]
            right = [list(x) for x in a]
            left[i][1] = b[i][0] - 1
            right[i][0] = b[i][0]
            ret.append(tuple(tuple(x) for x in left))
            a = right

        if a[i][0] <= b[i][1] < a[i][1]:
            left = [list(x) for x in a]
            right = [list(x) for x in a]
            left[i][1] = b[i][1]
            right[i][0] = b[i][1] + 1
            ret.append(tuple(tuple(x) for x in right))
            a = left
    # a is now a n b
    return ret


def volume(cell: Cuboid):
    ((x0, x1), (y0, y1), (z0, z1)) = cell
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def l_volume(l: list[Cuboid]):
    return sum(volume(cell) for cell in l)


def part2() -> int:
    # a list of non-intersecting cuboids of on cells
    on_list = []
    data = parse_lines()
    for cmd, line in otqdm(data):
        if cmd:
            cells_to_add = [line]
            for on_cell in on_list:
                new_cells_to_add = []
                for add_cell in cells_to_add:
                    if cuboid_intersection(add_cell, on_cell):
                        new_cells_to_add += cuboid_difference(add_cell, on_cell)
                    else:
                        new_cells_to_add.append(add_cell)
                cells_to_add = new_cells_to_add
            on_list += cells_to_add

        else:
            new_on_list = []
            for on_cell in on_list:
                if cuboid_intersection(on_cell, line):
                    new_on_list += cuboid_difference(on_cell, line)
                else:
                    new_on_list.append(on_cell)
            on_list = new_on_list

    return sum(volume(cell) for cell in on_list)


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
