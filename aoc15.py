def open_txt(filename: str) -> list[int]:
    with open(filename, "r") as f:
        starting = f.readline().rstrip()
        return list(int(x) for x in starting.split(","))

def memory_game(starting: list[int], n_th: int):
    prev_numbers = dict()
    for idx, num in enumerate(starting[:-1], start=1):
        prev_numbers[num] = idx
    i = len(starting)
    number = starting[-1]
    while i < n_th:
        # print(f"{i}th: {number}")
        if not prev_numbers.get(number):
            prev_numbers[number] = i
            number = 0
        else:
            tmp = i - prev_numbers.get(number)
            prev_numbers[number] = i
            number = tmp
        i += 1
    print(len(prev_numbers))
    return number

if __name__ == "__main__":
    # starting = open_txt("test.txt")
    starting = open_txt("aoc15.txt")
    print("part 1: ", memory_game(starting, 2020))
    print("part 2: ", memory_game(starting, 30000000))
