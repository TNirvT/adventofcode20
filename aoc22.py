from typing import NamedTuple

class Cards(NamedTuple):
    p1: list[int]
    p2: list[int]

def open_txt(filename: str):
    lines: list[list]
    lines = []
    with open(filename, "r") as f:
        for line in f:
            if "Player" in line:
                lines.append([])
            elif line.rstrip().isnumeric():
                lines[-1].append(int(line.rstrip()))
    return Cards(lines[0], lines[1])

def score(player: list[int]) -> int:
    result = 0
    for idx, num in enumerate(player[::-1], 1):
        result += idx * num
    return result

def part1(cards: Cards):
    while cards.p1 and cards.p2:
        card1 = cards.p1.pop(0)
        card2 = cards.p2.pop(0)
        if card1 > card2:
            cards.p1.append(card1)
            cards.p1.append(card2)
        elif card2 > card1:
            cards.p2.append(card2)
            cards.p2.append(card1)
        else:
            raise AssertionError("cards are equal")

    if cards.p1:
        return score(cards.p1)
    else:
        return score(cards.p2)

def part2(cards: Cards):
    
    return

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc22.txt")
    print("part 1: ", part1(lines))
