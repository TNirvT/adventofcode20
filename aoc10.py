def open_txt(filename: str) -> list[int]:
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(int(line))
    return lines

def part_one(lines: list[int]) -> int:
    lines_sorted = sorted([0] + lines)
    count1, count3 = 0, 1
    for i in range(len(lines_sorted) - 1):
        if lines_sorted[i+1] - lines_sorted[i] == 1:
            count1 += 1
        elif lines_sorted[i+1] - lines_sorted[i] == 3:
            count3 += 1
    return count1 * count3 # 1-jolt differences * 3-jolt differences

def graph(lines: list[int]):
    g = dict()
    for i in lines:
        g[i] = {x for x in range(i+1, i+4) if x in lines}
        # such that the last node (largest joltage) will always has a value of empty set
    return g

count = 0

def dfs_allpath(g: dict, start: int, end: int, visited: set=set()):
    global count
    visited.add(start)

    if start == end:
        # print(*path, sep=" ->")
        count += 1
    else:
        for node in g[start]:
            if node not in visited:
                # dfs_allpath(g, node, end, visited, path)
                dfs_allpath(g, node, end, visited)

    visited -= {start}
    return

def dfs(g: dict, start: int, visited: dict=dict()):
    if start in visited:
        return visited[start]
    if g[start]: # i.e. not the last node (largest joltage), since bool(set()) == False
        count = 0
        for node in g[start]:
            count += dfs(g, node, visited)
        visited[start] = count
        # visited[start] = sum(dfs(g, x, visited) for x in g[start])
        return visited[start]
    else: # i.e. start == last node
        return 1

if __name__ == "__main__":
    lines = open_txt("test.txt")
    lines = open_txt("aoc10.txt")
    print("part 1: ", part_one(lines))

    lines += [0]
    lines.sort()
    g = graph(lines)
    count = 0
    # dfs_allpath(g, 0, max(lines))
    count = dfs(g, 0)
    print("count: ", count)
