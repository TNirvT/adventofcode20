import re

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
                    # rules[int(idx)] = [[int(y) for y in x.split()] for x in seq.split("|")]
            else:
                msgs.append(line.rstrip())
    return rules, msgs

def dfs(rules: dict[int, str | list[int, str]], idx: int=0):
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
