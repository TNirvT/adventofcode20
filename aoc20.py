import random
from typing import NamedTuple

def open_txt(filename: str):
    tiles = dict()
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            if "Tile" in line:
                [_, tile_id] = line.split()
                tile_id = int(tile_id[:-1])
                tiles[tile_id] = []
            elif line:
                tiles[tile_id].append(line)
    return tiles

class Borders(NamedTuple):
    up: str
    down: str
    left: str
    right: str

def get_borders(tile: list[str]):
    left, right = "", ""
    for line in tile:
        left += line[0]
        right += line[-1]
    return Borders(tile[0], tile[-1], left, right)

def get_all_borders(tiles: dict[int, list[str]]) -> dict[int, Borders]:
    borders = dict(zip(tiles.keys(), [None] * len(tiles)))
    for tile_id, tile in tiles.items():
        borders[tile_id] = get_borders(tile)
    return borders

def rotate(borders: Borders, i: int) -> Borders:
    if i == 1: # anti-clockwise 1
        return Borders(borders.right, borders.left, borders.up[::-1], borders.down[::-1])
    elif i == 2:
        return Borders(borders.down[::-1], borders.up[::-1], borders.right[::-1], borders.left[::-1])
    elif i == 3:
        return Borders(borders.left[::-1], borders.right[::-1], borders.down, borders.up)

def flip(borders: Borders, i: int) -> Borders:
    if i == 1: # up-down flip
        return Borders(borders.down, borders.up, borders.left[::-1], borders.right[::-1])
    elif i == 2: # left-right flip
        return Borders(borders.up[::-1], borders.down[::-1], borders.right, borders.left)

def compare_borders(borders1: Borders, borders2: Borders):
    # 0: up, 1: down, 2: left, 3: right
    for i, border in enumerate(borders2):
        if border in borders1:
            if border == borders1.up:
                if i == 1: # borders2.down == borders1.up
                    return 0, borders2
                elif i == 0:
                    return 0, flip(borders2, 1)
                elif i == 2:
                    return 0, rotate(borders2, 1)
                else:
                    return 0, rotate(borders2, 3)
            elif border == borders1.down:
                if i == 0: # borders2.up == borders1.down
                    return 1, borders2
                elif i == 1:
                    return 1, flip(borders2, 1)
                elif i == 2:
                    return 1, flip(rotate(borders2, 3), 2)
                else:
                    return 1, rotate(borders2, 1)
            elif border == borders1.left:
                if i == 3: # borders2.right == borders1.left
                    return 2, borders2
                elif i == 0:
                    return 2, rotate(borders2, 3)
                elif i == 1:
                    return 2, flip(rotate(borders2, 1), 1)
                else:
                    return 2, flip(borders2, 2)
            else:
                if i == 2: # borders2.left == borders1.right
                    return 3, borders2
                elif i == 0:
                    return 3, flip(rotate(borders2, 1), 1)
                elif i == 1:
                    return 3, rotate(borders2, 3)
                else:
                    return 3, flip(borders2, 2)

        elif border[::-1] in borders1:
            border = border[::-1]
            if border == borders1.up:
                if i == 0: # borders2.up[::-1] == borders1.up
                    return 0, rotate(borders2, 2)
                elif i == 1:
                    return 0, flip(borders2, 2)
                elif i == 2:
                    return 0, flip(rotate(borders2, 1), 2)
                else:
                    return 0, rotate(borders2, 3)
            elif border == borders1.down:
                if i == 0: # borders2.up[::-1] == borders1.down
                    return 1, flip(borders2, 2)
                elif i == 1:
                    return 1, rotate(borders2, 2)
                elif i == 2:
                    return 1, rotate(borders2, 3)
                else:
                    return 1, flip(rotate(borders2, 1), 2)
            elif border == borders1.left:
                if i == 0: # borders2.up[::-1] == borders1.left
                    return 2, flip(rotate(borders2, 1), 3)
                elif i == 1:
                    return 2, rotate(borders2, 1)
                elif i == 2:
                    return 2, rotate(borders2, 2)
                else:
                    return 2, flip(borders2, 1)
            else:
                if i == 0: # borders2.up[::-1] == borders1.right
                    return 3, rotate(borders2, 1)
                elif i == 1:
                    return 3, flip(rotate(borders2, 3), 1)
                elif i == 2:
                    return 3, flip(borders2, 1)
                else:
                    return 3, rotate(borders2, 2)

def assemble_image_old(tiles: dict[int, list[str]]) -> list[list[int]]:
    borders = get_all_borders(tiles)
    tiles_pool = list(tiles.keys())
    start = random.choice(tiles_pool)
    tiles_pool.remove(start)
    i, j = 0, 0
    result = {(i, j): start}
    for tile_id in tiles_pool:
        compared = compare_borders(borders[start], borders[tile_id])
        if compared:
            direction, rearranged = compared
            if direction == 0:
                result[i, j-1] = tile_id
            if direction == 1:
                result[i, j+1] = tile_id
            if direction == 2:
                result[i-1, j] = tile_id
            if direction == 3:
                result[i+1, j] = tile_id

    return result

def has_common_border(borders1: Borders, borders2: Borders) -> bool:
    for border in borders2:
        if border in borders1:
            return True
        elif border[::-1] in borders1:
            return True
    return False

def assemble_image(tiles: dict[int, list[str]]):
    borders = get_all_borders(tiles)
    result: dict[int, list[int]]
    result = dict()
    for tile_id in borders:
        for another_id in borders:
            if has_common_border(borders[tile_id], borders[another_id]) and tile_id != another_id:
                if tile_id not in result:
                    result[tile_id] = [another_id]
                else:
                    result[tile_id].append(another_id)
    return result

def part1(image: dict[int, list[int]]) -> int:
    result = 1
    for tile_id, neighbors in image.items():
        if len(neighbors) == 2:
            print(tile_id)
            result *= tile_id
    return result

if __name__ == "__main__":
    # tiles = open_txt("test.txt")
    tiles = open_txt("aoc20.txt")
    image = assemble_image(tiles)
    print("part 1: ", part1(image))
