import random
import re
from typing import NamedTuple
from functools import reduce

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

def common_border(borders1: Borders, borders2: Borders) -> str | None:
    for border in borders2:
        if border in borders1:
            return border[:]
        elif border[::-1] in borders1:
            return border[::-1]
    return None

def rotate_tile(tile: list[str], rotation: int) -> list[str]:
    if rotation not in (1, 2, 3):
        raise ValueError("rotate only 1 / 2 / 3 times")

    if rotation == 1: # anti-clockwise by 90 deg
        return ["".join(x[-1-i] for x in tile) for i in range(len(tile))]
    elif rotation == 2:
        return [x[::-1] for x in tile][::-1]
    else:
        return ["".join(x[i] for x in tile)[::-1] for i in range(len(tile))]

def flip_tile(tile: list[str], direction: int) -> list[str]:
    # direction 1 = up-down flip, 2 = left-right flip
    if direction not in (1, 2):
        raise ValueError("flip only 1(up-down) / 2(left-right)")

    if direction == 1:
        return tile[::-1]
    else:
        return [x[::-1] for x in tile]

def transform_tile(tile: list[str]) -> list[list[str]]:
    return [tile, rotate_tile(tile, 1), rotate_tile(tile, 2), rotate_tile(tile, 3), flip_tile(tile, 1), flip_tile(tile, 2), flip_tile(rotate_tile(tile, 1), 1), flip_tile(rotate_tile(tile, 1), 2)]

class Image:
    def __init__(self, tiles: dict[int, list[str]]) -> None:
        self.tiles = tiles
        self.borders = get_all_borders(tiles)
        self.image = self.assemble_image()

    def assemble_image(self) -> dict[int, list[int]]:
        image: dict[int, list[int]]
        image = dict()
        for tile_id in self.borders:
            for another_id in self.borders:
                if common_border(self.borders[tile_id], self.borders[another_id]) is not None and tile_id != another_id:
                    if tile_id not in image:
                        image[tile_id] = [another_id]
                    else:
                        image[tile_id].append(another_id)
        return image

    def _corner_top_left(self, corner_id) -> None:
        [neighbor1, neighbor2] = self.image[corner_id]
        for transform in transform_tile(self.tiles[corner_id]):
            borders = get_borders(transform)
            common1 = common_border(borders, self.borders[neighbor1])
            common2 = common_border(borders, self.borders[neighbor2])
            if (common1 == borders.right and common2 == borders.down) or (common1 == borders.down and common2 == borders.right):
                self.borders[corner_id] = borders
                self.tiles[corner_id] = transform
                return
        raise AssertionError("cannot transform to top-left corner")

    def _add_tile_to_right(self, current: int, next: int, row: list[str]):
        for transform in transform_tile(self.tiles[next]):
            transform_borders = get_borders(transform)
            if transform_borders.left == self.borders[current].right:
                tmp = [x[1:-1] for x in transform[1:-1]]
                self.borders[next] = transform_borders
                self.tiles[next] = transform
                return [row[i] + tmp[i] for i in range(len(row))]
        raise AssertionError("can't add tile to the row")

    def image_row(self, current: int, row: list[str]=[]) -> list[str]:
        if not row:
            self.visited.add(current)
            row = [x[1:-1] for x in self.tiles[current][1:-1]]
            for neighbor in self.image[current]:
                if neighbor not in self.visited:
                    common = common_border(self.borders[current], self.borders[neighbor])
                    if common == self.borders[current].right:
                        next = neighbor
                        break
            self.visited.add(next)
            row = self._add_tile_to_right(current, next, row)
            return self.image_row(next, row)

        for neighbor in self.image[current]:
            if neighbor not in self.visited:
                if common_border(self.borders[current], self.borders[neighbor]) == self.borders[current].right:
                    if len(self.image[neighbor]) < len(self.image[current]):
                        self.visited.add(neighbor)
                        return self._add_tile_to_right(current, neighbor, row)

                    self.visited.add(neighbor)
                    row = self._add_tile_to_right(current, neighbor, row)
                    return self.image_row(neighbor, row)
        raise AssertionError("this should never appear") # debug

    def final_image(self, start: int) -> list[str]:
        self._corner_top_left(start)
        final_image = []
        self.visited = set()
        while True:
            final_image += self.image_row(start)
            prev_down = self.borders[start].down[:]
            tmp = set(self.image[start]).difference(self.visited)
            if tmp:
                start = tmp.pop()
                for transform in transform_tile(self.tiles[start]):
                    borders = get_borders(transform)
                    if borders.up == prev_down:
                        self.borders[start] = borders
                        self.tiles[start] = transform
            else:
                break
        # del self.visited
        return final_image

def part1(image: dict[int, list[int]]) -> list[int]:
    result = []
    for tile_id, neighbors in image.items():
        if len(neighbors) == 2:
            result.append(tile_id)
    return result

def count_monster(final_image: list[str], monster_pattern: list[str]):
    count = 0
    for i, line in enumerate(final_image):
        if i > len(final_image) - len(monster_pattern) + 1:
            break

        for j in range(len(line) - len(monster_pattern[0]) + 1):
            if re.match(monster_pattern[0], line[j:]) and re.match(monster_pattern[1], final_image[i+1][j:]) and re.match(monster_pattern[2], final_image[i+2][j:]):
                count += 1
    return count

def part2(final_image: list[str]):
    monster = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]
    monster_sharp = 0
    monster_pattern = []
    for line in monster:
        monster_sharp += line.count("#")
        monster_pattern.append(line.replace(" ", "."))
    total_sharp = 0
    for line in final_image:
        total_sharp += line.count("#")

    for transform in transform_tile(final_image):
        count = count_monster(transform, monster_pattern)
        if count > 0:
            return total_sharp - (count * monster_sharp)

if __name__ == "__main__":
    # tiles = open_txt("test.txt")
    tiles = open_txt("aoc20.txt")
    image = Image(tiles)
    result = part1(image.image)
    print("part 1: ", reduce(lambda a, b: a*b, result))
    final_image = image.final_image(random.choice(result))
    print("part 2: ", part2(final_image))
