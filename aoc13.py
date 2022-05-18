from functools import reduce

def open_txt(filename: str, mode: str="r") -> tuple[int, list]:
    with open(filename, mode) as f:
        estimate = int(f.readline())
        lines = f.readline().split(sep=",")
        buses = [int(x) if x != "x" else "x" for x in lines]
    return estimate, buses

def earliest(start: int, buses: list):
    i = start
    while i < start * 100:
        for bus in buses:
            if isinstance(bus, int) and i % bus == 0:
                return (i - start) * bus
        i += 1

def earliest_contest_brute(buses: list):
    t = 0
    while True:
        t_tmp = t
        for i in range(len(buses)):
            if buses[i] != "x" and t_tmp % buses[i] != 0:
                break
            elif i == len(buses) - 1 and (buses[-1] == "x" or t_tmp % buses[-1] == 0):
                return t
            t_tmp += 1
        t += buses[0]

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1

def part2_chinese_remainder(buses: list[int, str]):
    buses_id = [i for i in buses if i != "x"]
    remainders = [buses[i] - i for i in range(len(buses)) if buses[i] != "x"]
    return chinese_remainder(buses_id, remainders)

# 7,13,x,x,59,x,31,19
# 7     *n1 = t
# 13    *n2 = t + 1
# 59    *n3 = t + 4 ...

# t % 7 = 0
# t % 13 = 1
# t % 59 = 4 ...

# N = 7*13*59*31*19 = 3162341

if __name__ == "__main__":
    # estimate, buses = open_txt("test.txt")
    estimate, buses = open_txt("aoc13.txt")
    print("part 1: ", earliest(estimate, buses))
    # print("part 2: ", earliest_contest_brute(buses))
    print("part 2: ", part2_chinese_remainder(buses))
