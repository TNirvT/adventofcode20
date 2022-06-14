import re
from copy import deepcopy

def open_txt(filename: str):
    rules = dict()
    msgs = []
    with open(filename, "r") as f:
        for line in f:
            if ':' in line:
                [idx, seq] = line.rstrip().split(sep=": ")
                if '"' in line:
                    seq = seq.strip()
                    seq = seq.replace('"', '')
                    rules[int(idx)] = seq
                else:
                    rules[int(idx)] = [int(x) if x.isnumeric() else x for x in seq.split()]
            else:
                msgs.append(line.rstrip())
    return rules, msgs

def dfs(rules: dict[int, str | list[int, str]], idx: int=0) -> str:
    # if idx in {8, 11, 31, 42}:  # debug
    #     print(f"searched index {idx}")

    if isinstance(rules[idx], str):
        return rules[idx]

    if "|" not in rules[idx]:
        return "".join(dfs(rules, x) for x in rules[idx])
    else:
        result = ["("] + [dfs(rules, x) if x != "|" else "|" for x in rules[idx]] + [")"]
        return "".join(result)

def part1(pattern: str, msgs: list[str]):
    count = 0
    for msg in msgs:
        if re.fullmatch(pattern, msg):
            count += 1
    return count

def re_len(pattern: str) -> int:
    length = 0
    pipe = False
    stack_count = 0
    for char in pattern:
        if not pipe:
            if char == "a" or char == "b":
                length += 1
            elif char == "|":
                pipe = True
                stack_count += 1
        else:
            if char == ")":
                stack_count -= 1
                if stack_count == 0:
                    pipe = False
            elif char == "(":
                stack_count += 1
    return length

def part2(rules: dict[int, list[int, str] | str]):
    new_rules = deepcopy(rules)
    r42_len = re_len(dfs(rules, 42))
    r31_len = re_len(dfs(rules, 31))
    """given: new_rules[8] = [42]"""
    for i in range(88 // r42_len):
        new_rules[8] += ["|"] + [42] * (i+2)
    """given: new_rules[11] = [42, 31]"""
    for i in range(88 // (r42_len + r31_len)):
        new_rules[11] += ["|"] + [42] * (i+2) + [31] * (i+2)
    return new_rules

if __name__ == "__main__":
    # rules, msgs = open_txt("test.txt")
    rules, msgs = open_txt("aoc19.txt")
    pattern = dfs(rules)
    # print(re.fullmatch(pattern, "ababbb"))
    # print(re.fullmatch(pattern, "abbbab"))
    # print(re.fullmatch(pattern, "bababa"))
    # print(re.fullmatch(pattern, "aaabbb"))
    # print(re.fullmatch(pattern, "aaaabbb"))
    print("part 1: ", part1(pattern, msgs))
    new_pattern = dfs(part2(rules))
    print("part 2: ", part1(new_pattern, msgs))
