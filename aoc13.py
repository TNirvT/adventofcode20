def open_txt(filename: str, mode: str="r") -> tuple[int, list]:
    with open(filename, mode) as f:
        estimate = int(f.readline())
        lines = f.readline().split(sep=",")
        buses = [int(x) if x != "x" else "x" for x in lines]
    return estimate, buses

def earliest(start: int, buses: list):
    i = start
    while i < start * 100:
        for bus in buses:
            if isinstance(bus, int) and i % bus == 0:
                return (i - start) * bus
        i += 1

if __name__ == "__main__":
    # estimate, buses = open_txt("test.txt")
    estimate, buses = open_txt("aoc13.txt")
    result = earliest(estimate, buses)
    print("part: ", result)
