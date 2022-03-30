# from collections import namedtuple

# Data = namedtuple("Data", ["policy", "password"])
# Policy = namedtuple("Policy", ["char", "low", "hi"])
# Data.__annotations__ = {"policy": Policy, "password": str}
# Policy.__annotations__ = {"cahr": str, "low": int, "hi": int}

from typing import NamedTuple

class Policy(NamedTuple):
    char: str
    low: int
    hi: int

class Data(NamedTuple):
    policy: Policy
    password: str

def open_txt(filename: str) -> list[Data[Policy, str]]:
    with open(filename) as f:
        lines = []
        for line in f:
            pw_policy, password = tuple(line.rstrip().split(": "))
            [values, key] = pw_policy.split()
            [lowest, highest] = values.split("-")
            lines.append(Data(Policy(key, int(lowest), int(highest)), password))
    return lines

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc02.txt")
    valid_count = 0
    for line in lines:
        policy_freq = line.password.count(line.policy.char)
        if policy_freq >= line.policy.low and policy_freq <= line.policy.hi:
            valid_count += 1
    print("part 1: ", valid_count)

    valid_count = 0
    for line in lines:
        char = line.policy.char
        if (line.password[line.policy.low-1] == char) != (line.password[line.policy.hi-1] == char):
            valid_count += 1
    print("part 2: ", valid_count)
