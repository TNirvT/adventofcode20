import re
from typing import NamedTuple

class Field(NamedTuple):
    name: str
    s1: int
    e1: int
    s2: int
    e2: int

def open_txt(filename: str) -> tuple[list[Field], list[int], list[list[int]]]:
    fields = []
    nearby = []
    with open(filename, "r") as f:
        while f:
            line = f.readline().rstrip()
            if line == "":
                break
            match = re.match(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line)
            field = match.group(1)
            s1, e1, s2, e2 = (int(x) for x in match.groups()[1:])
            fields.append(Field(field, s1, e1, s2, e2))

        f.readline()
        myticket = [int(x) for x in f.readline().rstrip().split(",")]

        f.readline()
        f.readline()
        while f:
            line = f.readline().rstrip()
            if line == "":
                break
            nearby.append([int(x) for x in line.split(",")])
    return fields, myticket, nearby

def num_is_invalid(num: int, fields: list[Field]) -> bool:
    for field in fields:
        if num in range(field.s1, field.e1 + 1) or num in range(field.s2, field.e2 + 1):
            return False
    return True

def part1(nearby: list[list[int]], fields: list[Field]):
    result = 0 
    for ticket in nearby:
        for num in ticket:
            if num_is_invalid(num, fields):
                result += num
    return result

def part2():
    return

if __name__ == "__main__":
    # fields, myticket, nearby = open_txt("test.txt")
    fields, myticket, nearby = open_txt("aoc16.txt")
    print("part 1: ", part1(nearby, fields))
