import random
from copy import deepcopy
from itertools import product

from utils import benchmark, debug_print, get_day

test = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

chunks = get_day(19, test).split("\n\n")
data = []
for chunk in chunks:
    _, *lines = chunk.split("\n")
    tmp = []
    for line in lines:
        tmp.append(tuple(map(int, line.split(","))))
    data.append(tmp)


def rotate(xyz: tuple[int, int, int], i: int):
    x, y, z = xyz
    # 4 90deg rotations, 6 faces
    rot, face = divmod(i, 6)

    if face == 0:
        x, y, z = x, y, z
    elif face == 1:
        x, y, z = y, z, x
    elif face == 2:
        x, y, z = z, x, y
    elif face == 3:
        x, y, z = -x, -z, -y
    elif face == 4:
        x, y, z = -y, -x, -z
    elif face == 5:
        x, y, z = -z, -y, -x
    else:
        raise Exception()

    if rot == 0:
        x, y = x, y
    elif rot == 1:
        x, y = -y, x
    elif rot == 2:
        x, y = -x, -y
    elif rot == 3:
        x, y = y, -x
    else:
        raise Exception()
    return x, y, z


def difference(a, b):
    return tuple(aa - bb for aa, bb in zip(a, b))


def add(a, b):
    return tuple(aa + bb for aa, bb in zip(a, b))


def transpose_list(l, v):
    return tuple(add(ll, v) for ll in l)


# # fixing rotations
# seen = set(rotate((1, 2, 3), i) for i in range(24))
# debug_print(len(seen))
# seen2 = set(rotate(xyz,i) for xyz, i in product(seen, range(24)))
# debug_print(len(seen2))


def part1():
    """
    we pick an origin scanner, call that the base group
    pick a random scanner candidate from the remaining scanners
        pick a random rotation and rotate the entire candidate
        rotation is expensive, so try the following several times
            pick a point in the base group
            pick a point in the scanner
            translate every point in the scanner so those two points overlap
            count the number of overlaps
            if the number of overlaps is greater than 12
                add the TRANSPOSED points to base group
                record the rotation and offset

    """
    other_scanners: list
    origin_scanner, *other_scanners = deepcopy(data)
    base_group = set(origin_scanner)

    while other_scanners:
        candidate_idx = random.randint(0, len(other_scanners) - 1)
        original_candidate = other_scanners[candidate_idx]
        rotation = random.randint(0, 24 - 1)
        candidate = tuple(rotate(xyz, rotation) for xyz in original_candidate)
        tbg = tuple(base_group)

        for _ in range(20):
            v0 = random.choice(candidate)
            v1 = random.choice(tbg)
            # vector FROM candidate TO base group
            v = difference(v1, v0)
            candidate2 = transpose_list(candidate, v)
            overlap_count = len(base_group.intersection(candidate2))
            if overlap_count > 11:
                other_scanners.pop(candidate_idx)
                base_group.update(candidate2)
                debug_print(f"{rotation=} {v=}")
                debug_print(f"remaining={len(other_scanners)}")
                break
    return len(base_group)


def manhat(v1, v2):
    return sum(abs(a - b) for a, b in zip(v1, v2))


def part2():
    other_scanners: list
    origin_scanner, *other_scanners = deepcopy(data)
    base_group = set(origin_scanner)

    v_list = [(0, 0, 0)]
    while other_scanners:
        candidate_idx = random.randint(0, len(other_scanners) - 1)
        original_candidate = other_scanners[candidate_idx]
        rotation = random.randint(0, 24 - 1)
        candidate = tuple(rotate(xyz, rotation) for xyz in original_candidate)
        tbg = tuple(base_group)
        for _ in range(20):
            v0 = random.choice(candidate)
            v1 = random.choice(tbg)
            v = difference(v1, v0)
            candidate2 = transpose_list(candidate, v)
            overlap_count = len(base_group.intersection(candidate2))
            if overlap_count > 11:
                other_scanners.pop(candidate_idx)
                base_group.update(candidate2)
                v_list.append(v)
                debug_print(f"{rotation=} {v=}")
                debug_print(f"remaining={len(other_scanners)}")
                break

    return max(manhat(v1, v2) for v1, v2 in product(v_list, v_list))


benchmark(part1)
benchmark(part2)
