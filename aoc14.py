from typing import NamedTuple
import re

class MemValue(NamedTuple):
    address: int
    value: int

class Session(NamedTuple):
    mask: str
    lines: list[MemValue]

def open_txt(filename: str) -> tuple[str, list]:
    with open(filename, "r") as f:
        sessions = []
        for line in f:
            if line.split()[0] == "mask":
                mask_raw = line.rstrip()
                mask = mask_raw.split(sep=" = ")[1]
                sessions.append(Session(mask, []))
            else:
                line = re.findall(r"\d+", line.rstrip())
                sessions[-1].lines.append(MemValue(int(line[0]), int(line[1])))

    return sessions

def masking(dec_value: int, mask: str) -> str:
    bi_value = format(dec_value, f"0{len(mask)}b")
    for i in range(len(mask)):
        if mask[i] != "X":
            tmp = list(bi_value)
            tmp[i] = mask[i]
            bi_value = "".join(tmp)
    return bi_value

def writing_mem(sessions: list[Session]) -> dict:
    mem = dict()
    for session in sessions:
        mask = session.mask
        for line in session.lines:
            mem[line.address] = masking(line.value, mask)
    return mem

if __name__ == "__main__":
    # sessions = open_txt("test.txt")
    sessions = open_txt("aoc14.txt")
    mem = writing_mem(sessions)
    print("part 1: ", sum([int(x, 2) for x in mem.values()]))
