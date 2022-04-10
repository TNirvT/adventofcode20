from itertools import combinations



def open_txt(filename: str) -> list[int]:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(int(line))
    return lines

def not_follow_rule(lines: list[int], n: int) -> int:
    for i in range(n, len(lines)):
        combos = combinations(lines[i-n:i], 2)
        combos_set = {sum(x) for x in combos}
        if lines[i] not in combos_set:
            return lines[i]

def weakness(lines: list[int], number: int) -> int:
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            tmp_list = lines[i:j]
            if sum(tmp_list) == number:
                return max(tmp_list) + min(tmp_list)

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc09.txt")
    result = not_follow_rule(lines, 25)
    print("part 1: ", result)
    print("part 2: ", weakness(lines, result))

