def open_txt(filename: str) -> list[str]:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
    return lines

def move_in_direction(line: str, x: int, y: int):
    if line[0] == "N":
        y += int(line[1:])
    elif line[0] == "S":
        y -= int(line[1:])
    elif line[0] == "E":
        x += int(line[1:])
    elif line[0] == "W":
        x -= int(line[1:])
    else:
        raise AssertionError
    return x, y

NESW = {0: "E", 1: "S", 2: "W", 3: "N"}

def navigate(lines: list[str]):
    # East = 0, South = 1, West = 2, North = 3
    facing = 0
    ferry_x, ferry_y = 0, 0
    for line in lines:
        if line[0] == "L":
            facing -= int(line[1:]) // 90
            facing = facing % 4
        elif line[0] == "R":
            facing += int(line[1:]) // 90
            facing = facing % 4
        elif line[0] == "F":
            ferry_x, ferry_y = move_in_direction(NESW[facing] + line[1:], ferry_x, ferry_y)
        else:
            ferry_x, ferry_y = move_in_direction(line, ferry_x, ferry_y)
    return facing, ferry_x, ferry_y

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc12.txt")
    facing, ferry_x, ferry_y = navigate(lines)
    print("part 1: ", abs(ferry_x) + abs(ferry_y))
