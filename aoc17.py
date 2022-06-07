import itertools
from typing import NamedTuple

def open_txt(filename: str):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def get_neighbors_pt1(node: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    tmp = [x for x in itertools.product((-1, 0, 1), repeat=3)]
    tmp.remove((0, 0, 0))
    neighbors = set(tuple(sum(x) for x in zip(node, vect)) for vect in tmp)
    return neighbors

def get_neighbors_pt2(node: tuple[int, int, int, int]) -> set[tuple[int, int, int, int]]:
    tmp = [x for x in itertools.product((-1, 0, 1), repeat=4)]
    tmp.remove((0, 0, 0, 0))
    neighbors = set(tuple(sum(x) for x in zip(node, vect)) for vect in tmp)
    return neighbors

def one_cycle(active_nodes: set[tuple], part=1) -> None:
        energy = dict()

        if part == 1:
            get_neighbors = get_neighbors_pt1
        elif part == 2:
            get_neighbors = get_neighbors_pt2

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

def part1(lines: list[str]):
    active_nodes = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                active_nodes.add((j, -i, 0))

    for _ in range(6):
        one_cycle(active_nodes)

    return len(active_nodes)

def part2(lines: list[str]):
    active_nodes = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                active_nodes.add((j, -i, 0, 0))

    for _ in range(6):
        one_cycle(active_nodes, part=2)

    return len(active_nodes)

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc17.txt")
    print("part 1: ", part1(lines))
    print("part 2: ", part2(lines))
