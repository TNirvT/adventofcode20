import itertools
from typing import NamedTuple

def open_txt(filename: str):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

class Bound(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

def part1(lines: list[str]):
    def get_neighbors(node: tuple[int, int, int]) -> set[tuple[int, int, int]]:
        tmp = [x for x in itertools.product((-1, 0, 1), repeat=3)]
        tmp.remove((0, 0, 0))
        neighbors = set(tuple(sum(x) for x in zip(node, vect)) for vect in tmp)
        return neighbors

    active_nodes = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                active_nodes.add((j, -i, 0))

    # bound_tmp = list(map(set, zip(*active_nodes))) # decompose to for-loops
    # bound_tmp = [(min(x), max(x)) for x in bound_tmp]
    # bound = Bound(bound_tmp[0][0], bound_tmp[0][1], bound_tmp[1][0], bound_tmp[1][1], bound_tmp[2][0], bound_tmp[2][1])
    # print(bound)

    def one_cycle(active_nodes: set[tuple[int, int, int]]) -> None:
        energy = dict()
        for node in active_nodes:
            neighbors = get_neighbors(node)
            for neighbor in neighbors:
                if energy.get(neighbor):
                    energy[neighbor] += 1
                else:
                    energy[neighbor] = 1

        for node in active_nodes:
            if node not in energy.keys():
                energy[node] = 0

        for node, level in energy.items():
            if node in active_nodes and level != 2 and level != 3:
                active_nodes.remove(node)
            elif node not in active_nodes and level == 3:
                active_nodes.add(node)

    for _ in range(6):
        one_cycle(active_nodes)

    return len(active_nodes)

def part2(lines: list[str]):
    def get_neighbors(node: tuple[int, int, int, int]) -> set[tuple[int, int, int, int]]:
        tmp = [x for x in itertools.product((-1, 0, 1), repeat=4)]
        tmp.remove((0, 0, 0, 0))
        neighbors = set(tuple(sum(x) for x in zip(node, vect)) for vect in tmp)
        return neighbors

    active_nodes = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                active_nodes.add((j, -i, 0, 0))

    def one_cycle(active_nodes: set[tuple[int, int, int, int]]) -> None:
        energy = dict()
        for node in active_nodes:
            neighbors = get_neighbors(node)
            for neighbor in neighbors:
                if energy.get(neighbor):
                    energy[neighbor] += 1
                else:
                    energy[neighbor] = 1

        for node in active_nodes:
            if node not in energy.keys():
                energy[node] = 0

        for node, level in energy.items():
            if node in active_nodes and level != 2 and level != 3:
                active_nodes.remove(node)
            elif node not in active_nodes and level == 3:
                active_nodes.add(node)

    for _ in range(6):
        one_cycle(active_nodes)

    return len(active_nodes)

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc17.txt")
    print("part 1: ", part1(lines))
    print("part 2: ", part2(lines))
