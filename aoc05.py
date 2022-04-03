def open_txt(filename: str) -> list:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines

def binary_space(line: str) -> tuple[int, int]:
    lo, hi = 0, 127
    for i in range(7):
        if line[i] == "F":
            hi = hi - (hi - lo + 1) // 2
        elif line[i] == "B":
            lo = lo + (hi - lo + 1) // 2
        else:
            raise ValueError("Expect F or B")
    r = lo

    lo, hi = 0, 7
    for i in range(7, 10):
        if line[i] == "L":
            hi = hi - (hi - lo + 1) // 2
        elif line[i] == "R":
            lo = lo + (hi - lo + 1) // 2
        else:
            raise ValueError("Expect L or R")
    c = lo
    return r, c

def seat_id(r: int, c: int) -> int:
    return r * 8 + c

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc05.txt")
    results = []
    for line in lines:
        r, c = binary_space(line)
        results.append(seat_id(r, c))
    print("part 1: ", max(results))

    # seats on row 0: 0~7
    # seats on row 127: 127*44~127*44 + 7 = 5588~5595
    my_seats = set()
    for seat in results:
        if seat > 7 and seat < 5588:
            if seat + 2 in results and seat + 1 not in results:
                my_seats.add(seat + 1)
            elif seat - 2 in results and seat - 1 not in results:
                my_seats.add(seat - 1)
    if len(my_seats) == 1:
        print("part 2: ", *my_seats)
    else:
        raise ValueError("More one possible seat is mine")
