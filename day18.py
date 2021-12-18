from utils import benchmark, debug_print, get_day

test = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

lines = get_day(18, test).split("\n")


class Node:
    def __init__(
        self, left: "Node" or int, right: "Node" or int, parent: "Node" or None = None
    ):
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        return f"[{self.left},{self.right}]"


# never creates a node, no keep track of parent
def explode(n: Node):
    l, r = n.left, n.right
    p = n
    while p.parent is not None and p.parent.left == p:
        p = p.parent
    if p.parent is None:  # there is not left-er node
        pass
    else:
        if isinstance(p.parent.left, int):
            p.parent.left += l
        else:
            p = p.parent.left
            while isinstance(p.right, Node):
                p = p.right
            p.right += l

    p = n
    while p.parent is not None and p.parent.right == p:
        p = p.parent
    if p.parent is None:  # there is no right-er node
        pass
    else:
        if isinstance(p.parent.right, int):
            p.parent.right += r
        else:
            p = p.parent.right
            while isinstance(p.left, Node):
                p = p.left
            p.left += r
    if n.parent:
        if n.parent.left == n:
            n.parent.left = 0
        elif n.parent.right == n:
            n.parent.right = 0
        else:
            raise Exception()


def split(x: int, parent: Node):
    return Node(x // 2, x - x // 2, parent)


def magnitude(x: Node or int):
    if isinstance(x, int):
        return x
    return 3 * magnitude(x.left) + 2 * magnitude(x.right)


def parse(line: str):
    as_lists = eval(line)
    return parse_list(as_lists)


# parent check
def parse_list(l: list or int, parent=None):
    if isinstance(l, int):
        return l
    node = Node(-1, -1, parent)
    node.left = parse_list(l[0], node)
    node.right = parse_list(l[1], node)
    return node


def first_nested(node: Node, depth=4):
    if depth > 0:  # not deep enough
        if isinstance(node.left, Node):
            val = first_nested(node.left, depth - 1)
            if val is not None:
                return val
        if isinstance(node.right, Node):
            val = first_nested(node.right, depth - 1)
            if val is not None:
                return val
    else:
        while True:  # has to exit
            while isinstance(node.left, Node):
                node = node.left
            # left is now an int
            if isinstance(node.right, int):
                return node
            else:
                node = node.right


def found_first_split(node: Node) -> bool:
    if isinstance(node.left, int):
        if node.left >= 10:
            node.left = split(node.left, node)
            return True
    elif found_first_split(node.left):  # left is node
        return True
    # left not helpful
    if isinstance(node.right, int):
        if node.right >= 10:
            node.right = split(node.right, node)
            return True
    elif found_first_split(node.right):
        return True
    return False


def simplify(node: Node):
    done = False
    while not done:
        fn = first_nested(node)
        if fn is not None:
            explode(fn)
            debug_print("after explode: ", node)
            continue
        if not found_first_split(node):
            # no node to explode or split
            done = True
        else:
            debug_print("after split:   ", node)
    return node
    # dfs for explode, split


def part1():
    data = tuple(map(parse, lines))

    runtot = data[0]
    simplify(runtot)
    if str(runtot) != lines[0]:
        raise Exception(str(runtot) + "\n" + lines[0])
    for num in data[1:]:
        parent = Node(runtot, num, None)
        num.parent = parent
        runtot.parent = parent
        debug_print("after addition:", parent)
        simplify(parent)
        debug_print("simplified:    ", runtot)
        runtot = parent

    return magnitude(runtot)


def parse_and_add(l1, l2):
    n1, n2 = parse(l1), parse(l2)
    parent = Node(n1, n2, None)
    n1.parent = parent
    n2.parent = parent
    return magnitude(simplify(parent))


def part2():
    def gen():
        for l1 in lines:
            for l2 in lines:
                if l1 != l2:
                    yield parse_and_add(l1, l2)

    return max(gen())


benchmark(part1)
# benchmark(part2)
