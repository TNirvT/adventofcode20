import re
import typing

def open_txt(filename: str):
    with open(filename) as f:
        lines = dict()
        for line in f:
            [k, v_list]= line.rstrip().split(sep="contain ")
            k = re.sub(r"\sbags?", r"", k).strip()
            v = dict()
            if v_list != "no other bags.":
                v_list = v_list.split(sep=", ")
                for bag in v_list:
                    k_tmp = re.search(r"[a-zA-Z\s]+(?=\sbag)", bag).group(0).strip()
                    v_tmp = int(re.search(r"\d+", bag).group(0))
                    v[k_tmp] = v_tmp
            lines[k] = v
    return lines

def least_one_bag(color: str, lines: typing.Dict[str, typing.Dict[str, int]]) -> int:
    if not lines[color]:
        return 0

    result = []
    for bag in lines[color]:
        if bag == "shiny gold":
            result.append(lines[color]["shiny gold"])
        else:
            result.append(least_one_bag(bag, lines))
    return sum(result)

def count_bags_inside(color: str, lines: typing.Dict[str, typing.Dict[str, int]]) -> int:
    if not lines[color]:
        return 0

    count = 0
    for bag in lines[color]:
        count += lines[color][bag]
        count += count_bags_inside(bag, lines) * lines[color][bag]
    return count

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc07.txt")
    count = 0
    for color in lines:
        if least_one_bag(color, lines) > 0:
            count += 1
    print("part 1: ", count)

    count = count_bags_inside("shiny gold", lines)
    print("part 2: ", count)
