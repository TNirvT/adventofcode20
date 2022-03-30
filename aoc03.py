def open_txt(filename: str):
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
    return lines

def traverse(lines: list, slope: tuple[int, int]):
    right, down = slope[0], slope[1]
    i, j = 0, 0
    bottom = len(lines) - 1
    tile_width = len(lines[0])

    tree_count = 0
    while i <= bottom:
        if lines[i][j] == "#":
            tree_count += 1
        j += right
        j = j % tile_width
        i += down
    return tree_count

if __name__ == "__main__":
    lines = open_txt("aoc03.txt")
    # lines = open_txt("test.txt")
    tree_count = traverse(lines, (3, 1))
    print("part 1: ", tree_count)

    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    result = 1
    for slope in slopes:
        tree_count = traverse(lines, slope)
        result *= tree_count
    print("part 2: ", result)
