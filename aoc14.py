from typing import NamedTuple
import re
from itertools import combinations, chain

class MemValue(NamedTuple):
    address: int
    value: int

class Mask(NamedTuple):
    mask0: int
    mask1: int
    maskX: int
    posX: list[int]

class Session(NamedTuple):
    mask: Mask
    lines: list[MemValue]

def open_txt(filename: str) -> list[Session]:
    with open(filename, "r") as f:
        sessions = []
        for line in f:
            if line.split()[0] == "mask":
                mask_raw = line.rstrip()
                mask = mask_raw.split(sep=" = ")[1]
                length = len(mask)
                mask0, mask1, maskX, posX = 0, 0, 0, []
                for i, b in enumerate(mask):
                    if b == "0":
                        mask0 += 1
                        # val &= ~mask0
                    elif b == "1":
                        mask1 += 1
                        # val |= mask1
                    elif b == "X":
                        maskX += 1
                        posX.append(2 ** (length - 1 - i))
                    mask0 <<= 1
                    mask1 <<= 1
                    maskX <<= 1
                mask0 >>= 1
                mask1 >>= 1
                maskX >>= 1
                sessions.append(Session(Mask(mask0, mask1, maskX, posX), []))
            else:
                line = re.findall(r"\d+", line.rstrip())
                sessions[-1].lines.append(MemValue(int(line[0]), int(line[1])))

    return sessions

def masking_string_op(dec_value: int, mask: str) -> str:
    bi_value = format(dec_value, f"0{len(mask)}b")
    for i in range(len(mask)):
        if mask[i] != "X":
            tmp = list(bi_value)
            tmp[i] = mask[i]
            bi_value = "".join(tmp)
    return bi_value

def masking(dec_value: int, mask: Mask) -> int: # bitwise op
    dec_value &= ~mask.mask0
    dec_value |= mask.mask1
    return dec_value

def writing_mem(sessions: list[Session]) -> dict:
    mem = dict()
    for session in sessions:
        for line in session.lines:
            mem[line.address] = masking(line.value, session.mask)
    return mem

def powerset(posX: list):
    return chain.from_iterable(combinations(posX, r) for r in range(len(posX)+1))

def masking_pt2(dec_value: int, mask: Mask) -> list[int]:
    dec_value &= ~mask.maskX
    dec_value |= mask.mask1
    result = []
    for combo in (sum(x) for x in powerset(mask.posX)):
        result.append(dec_value + combo)
    return result

def writing_mem_pt2(sessions: list[Session]):
    mem = dict()
    for session in sessions:
        for mem_val in session.lines:
            addresses = masking_pt2(mem_val.address, session.mask)
            for address in addresses:
                mem[address] = mem_val.value
    return mem

if __name__ == "__main__":
    # sessions = open_txt("test.txt")
    sessions = open_txt("aoc14.txt")
    mem = writing_mem(sessions)
    print("part 1: ", sum(x for x in mem.values()))
    mem = writing_mem_pt2(sessions)
    print("part 2: ", sum(x for x in mem.values()))
