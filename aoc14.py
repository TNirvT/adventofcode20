from typing import NamedTuple
import re
from itertools import combinations

class MemValue(NamedTuple):
    address: int
    value: int

class Session(NamedTuple):
    mask: str
    lines: list[MemValue]

class Mask(NamedTuple):
    mask0: int
    mask1: int
    maskX: int
    countX: int

def open_txt(filename: str) -> tuple[str, list]:
    with open(filename, "r") as f:
        sessions = []
        for line in f:
            if line.split()[0] == "mask":
                mask_raw = line.rstrip()
                mask = mask_raw.split(sep=" = ")[1]
                mask0, mask1, maskX, countX = 0, 0, 0, 0
                for b in mask:
                    if b == "0":
                        mask0 += 1
                        # val &= ~mask0
                    elif b == "1":
                        mask1 += 1
                        # val |= mask1
                    elif b == "X":
                        maskX += 1
                        countX += 1
                    mask0 <<= 1
                    mask1 <<= 1
                    maskX <<= 1
                mask0 >>= 1
                mask1 >>= 1
                maskX >>= 1
                sessions.append(Session(Mask(mask0, mask1, maskX, countX), []))
            else:
                line = re.findall(r"\d+", line.rstrip())
                sessions[-1].lines.append(MemValue(int(line[0]), int(line[1])))

    return sessions

def masking_old(dec_value: int, mask: str) -> str:
    bi_value = format(dec_value, f"0{len(mask)}b")
    for i in range(len(mask)):
        if mask[i] != "X":
            tmp = list(bi_value)
            tmp[i] = mask[i]
            bi_value = "".join(tmp)
    return bi_value

def masking(dec_value: int, mask: Mask) -> int:
    dec_value &= ~mask.mask0
    dec_value |= mask.mask1
    return dec_value

def writing_mem(sessions: list[Session]) -> dict:
    mem = dict()
    for session in sessions:
        mask = session.mask
        for line in session.lines:
            mem[line.address] = masking(line.value, mask)
    return mem

def masking_pt2(dec_value: int, mask: Mask) -> list[int]:
    dec_value ^= mask.mask0
    dec_value |= mask.mask1
    result = []
    bi_value = format(dec_value, "036b") # len(mask) = 36
    combos = combinations([0, 1], mask.countX)
    return result

def part2(sessions: list[Session]):
    mem = dict()
    for session in sessions:
        for memValue in session.lines:
                masking_pt2(memValue.value, session.mask)
    return

if __name__ == "__main__":
    # sessions = open_txt("test.txt")
    sessions = open_txt("aoc14.txt")
    mem = writing_mem(sessions)
    print("part 1: ", sum(x for x in mem.values()))
    part2(sessions)
