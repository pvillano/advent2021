from utils import benchmark, debug_print, get_day, debug_print_sparse_grid

test = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

algo_str, image_str = (
    get_day(20, test, override=False).replace("#", "1").replace(".", "0").split("\n\n")
)
image = image_str.split("\n")
algo: tuple[int] = tuple(map(int, algo_str))


def get_bits(i, j, sparse_image, spaaace):
    ret = 0
    for ii in range(i - 1, i + 2):
        for jj in range(j - 1, j + 2):
            ret <<= 1
            if (ii, jj) in sparse_image:
                ret += 1 - spaaace
            else:
                ret += spaaace
    return ret


def part1():
    spaaace = 0
    sparse_image = set()
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == "1":
                sparse_image.add((i, j))
    debug_print_sparse_grid(sparse_image, transpose=True)
    for i in range(2):
        new_space = algo[511 * spaaace]
        new_image = set()
        for i, j in sparse_image:
            for ii in range(i - 1, i + 2):
                for jj in range(j - 1, j + 2):
                    new_color = algo[get_bits(ii, jj, sparse_image, spaaace)]
                    if new_color != new_space:
                        new_image.add((ii, jj))
        sparse_image = new_image
        spaaace = new_space
        debug_print_sparse_grid(sparse_image, transpose=True)
    return len(sparse_image)


def part2():
    spaaace = 0
    sparse_image = set()
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == "1":
                sparse_image.add((i, j))
    for i in range(50):
        new_space = algo[511 * spaaace]
        new_image = set()
        for i, j in sparse_image:
            for ii in range(i - 1, i + 2):
                for jj in range(j - 1, j + 2):
                    new_color = algo[get_bits(ii, jj, sparse_image, new_space)]
                    if new_color != new_space:
                        new_image.add((ii, jj))
        sparse_image = new_image
        spaaace = new_space
    return len(sparse_image)


benchmark(part1)
benchmark(part2)
