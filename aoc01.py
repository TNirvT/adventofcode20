from itertools import combinations
import math

def open_txt(filename: str):
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(int(line.rstrip()))
    return lines

def sum_to_2020(lines: list, n: int) -> int:
    combos = combinations(lines, n)
    for combo in combos:
        if sum(combo) == 2020:
            return math.prod(combo)
    raise Exception("No solution")

if __name__ == "__main__":
    lines = open_txt("aoc01.txt")
    # lines = open_txt("test.txt")
    print("part 1: ", sum_to_2020(lines, 2))
    print("part 2: ", sum_to_2020(lines, 3))
