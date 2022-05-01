from itertools import combinations, product

DIRECTIONS = [
    (0, -1), #left
    (0, 1), #right
    (-1, 0), #up
    (1, 0), #down
    (-1, -1), #up-left
    (-1, 1), #up-right
    (1, -1), #down-left
    (1, 1) #down-right
]

def open_txt(filename: str) -> list[int]:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
    return lines

def adj_coord(i, l):
    if i == 0:
        return range(0, 2)
    elif i == l-1:
        return range(-1, 1)
    else:
        return range(-1, 2)

def get_no_of_occcupied(lines: list[str], i: int, j: int) -> int:
    adj_temp = list(product(adj_coord(i, len(lines)), adj_coord(j, len(lines[0]))))
    adj_temp.remove((0, 0))
    adjs = [(i+x, j+y) for x, y in adj_temp]

    count = 0
    for adj_i, adj_j in adjs:
        if lines[adj_i][adj_j] == "#":
            count += 1
    return count

def update_seats(lines: list[str]) -> list[str]:
    seats = []
    for i in range(len(lines)):
        line = ""
        for j in range(len(lines[0])):
            if lines[i][j] != ".":
                occupied = get_no_of_occcupied(lines, i, j)
                if occupied == 0:
                    line += "#"
                elif occupied >= 4:
                    line += "L"
                else:
                    line += lines[i][j]
            else:
                line += "."
        seats.append(line)
    return seats

def count_all_occupied(lines: list[str]) -> int:
    count = 0
    for line in lines:
        count += line.count("#")
    return count

def pt2_get_no_of_occcupied(lines: list[str], i: int, j: int) -> int:
    count = 0
    for dir_i, dir_j in DIRECTIONS:
        tmp_i, tmp_j = i, j
        seat = "."
        while seat == ".":
            tmp_i += dir_i
            tmp_j += dir_j
            if tmp_i >= 0 and tmp_i < len(lines) and tmp_j >=0 and tmp_j < len(lines[0]):
                seat = lines[tmp_i][tmp_j]
            else:
                break
            if seat == "#":
                count += 1
    return count

def pt2_update_seats(lines: list[str]) -> list[str]:
    seats = []
    for i in range(len(lines)):
        line = ""
        for j in range(len(lines[0])):
            if lines[i][j] != ".":
                occupied = pt2_get_no_of_occcupied(lines, i, j)
                if occupied == 0:
                    line += "#"
                elif occupied >= 5:
                    line += "L"
                else:
                    line += lines[i][j]
            else:
                line += "."
        seats.append(line)
    return seats

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc11.txt")
    seats = lines[:]
    while True:
        seats_tmp = update_seats(seats)
        if seats_tmp == seats:
            break
        else:
            seats = seats_tmp
    print("part 1: ", count_all_occupied(seats))
    seats = lines[:]
    while True:
        seats_tmp = pt2_update_seats(seats)
        if seats_tmp == seats:
            break
        else:
            seats = seats_tmp
    print("part 2: ", count_all_occupied(seats))
