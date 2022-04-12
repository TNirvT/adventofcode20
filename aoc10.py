def open_txt(filename: str) -> list[int]:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(int(line))
    return lines

def part_one(lines: list[int]) -> int:
    lines_sorted = sorted([0] + lines)
    count1, count3 = 0, 1
    for i in range(len(lines_sorted) - 1):
        if lines_sorted[i+1] - lines_sorted[i] == 1:
            count1 += 1
        elif lines_sorted[i+1] - lines_sorted[i] == 3:
            count3 += 1
    return count1 * count3 # 1-jolt differences x 3-jolt differences

if __name__ == "__main__":
    lines = open_txt("test.txt")
    lines = open_txt("aoc10.txt")
    print("part 1: ", part_one(lines))
