from typing import NamedTuple

class Cmd(NamedTuple):
    operation: str
    arg: int

def open_txt(filename: str) -> list[Cmd]:
    with open(filename) as f:
        lines = []
        for line in f:
            [operation, arg] = line.split()
            arg = int(arg)
            lines.append(Cmd(operation, arg))
    return lines

def accumulation(lines: list[Cmd]) -> tuple[int, bool]:
    acc = 0
    inf_loop = [False] * len(lines)

    i = 0
    while i < len(lines):
        if inf_loop[i]:
            break
        else:
            inf_loop[i] = True

        if lines[i].operation == "nop":
            i += 1
        elif lines[i].operation == "acc":
            acc += lines[i].arg
            i += 1
        elif lines[i].operation == "jmp":
            i += lines[i].arg
        else:
            raise ValueError("Undefined command")

    return acc, inf_loop[-1]

def terminate_trial(lines: list[Cmd], i: int) -> list[Cmd]:
    lines_new = lines[:]
    if lines[i].operation == "nop":
        lines_new[i] = Cmd("jmp", lines[i].arg)
    elif lines[i].operation == "jmp":
        lines_new[i] = Cmd("nop", lines[i].arg)
    else:
        lines_new = []
    return lines_new

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc08.txt")
    result, is_fixed = accumulation(lines)
    print("part 1: ", result)
    for i in range(len(lines)):
        lines_new = terminate_trial(lines, i)
        if lines_new:
            result, is_fixed = accumulation(lines_new)
            if is_fixed:
                print("part 2: ", result)
