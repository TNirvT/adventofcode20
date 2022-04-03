def open_txt(filename: str):
    with open(filename) as f:
        lines = [[]]
        for line in f:
            if line.rstrip() == "":
                lines.append([])
            else:
                lines[-1].append(line.rstrip())
    return lines

def count_yes(line: list[str]) -> int:
    counting_set = set()
    for answers in line:
        counting_set.update(set(answers))
    return len(counting_set)

def count_everyone_yes(line: list[str]) -> int:
    counting_string = line[0]
    for answers in line:
        for char in counting_string:
            if char not in answers:
                counting_string = counting_string.replace(char, "")
    return len(counting_string)

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc06.txt")
    count = 0
    for line in lines:
        count += count_yes(line)
    print("part 1: ", count)

    count = 0
    for line in lines:
        count += count_everyone_yes(line)
    print("part 2: ", count)
