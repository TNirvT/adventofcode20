import re
from typing import NamedTuple
import math
from copy import deepcopy

class Field(NamedTuple):
    name: str
    s1: int
    e1: int
    s2: int
    e2: int

def open_txt(filename: str) -> tuple[list[Field], list[int], list[list[int]]]:
    fields = []
    nearby = []
    with open(filename, "r") as f:
        while f:
            line = f.readline().rstrip()
            if line == "":
                break
            match = re.match(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line)
            field = match.group(1)
            s1, e1, s2, e2 = (int(x) for x in match.groups()[1:])
            fields.append(Field(field, s1, e1, s2, e2))

        f.readline()
        myticket = [int(x) for x in f.readline().rstrip().split(",")]

        f.readline()
        f.readline()
        while f:
            line = f.readline().rstrip()
            if line == "":
                break
            nearby.append([int(x) for x in line.split(",")])
    return fields, myticket, nearby

def num_is_invalid(num: int, fields: list[Field]) -> bool:
    for field in fields:
        if num in range(field.s1, field.e1 + 1) or num in range(field.s2, field.e2 + 1):
            return False
    return True

def part1(nearby: list[list[int]], fields: list[Field]):
    result = 0 
    for ticket in nearby:
        for num in ticket:
            if num_is_invalid(num, fields):
                result += num
    return result

def graph(data: dict) -> dict:
    # data is lhs -> rhs only, g is bi-directional
    g = deepcopy(data)
    for k, v in data.items():
        for neighbor in v:
            if not g.get(neighbor):
                g[neighbor] = [k]
            else:
                g[neighbor].append(k)
    return g

def graph_digital(data: dict) -> tuple[list[set[int]], dict]:
    # return a list of length = 1 + LHS + RHS
    # the 0-th element is a dummy vertex = empty list
    dict_revert = {x: i for (i, x) in enumerate(data.keys(), 1)}
    rhs = set()
    for neighbors in data.values():
        rhs |= set(neighbors)

    if len(data) > len(rhs):
        print("number of vertices on LHS > RHS")
    elif len(data) < len(rhs):
        print("number of vertices on LHS < RHS")

    dict_revert.update({x: i for (i, x) in enumerate(rhs, len(data)+1)})

    g_digital = [[]] * (1 + len(data) + len(rhs))
    for k, v in graph(data).items():
        g_digital[dict_revert[k]] = set(dict_revert[x] for x in v)

    return g_digital, dict(zip(dict_revert.values(), dict_revert.keys()))

def hopcroftkarp(data: dict):
    g, g_reverse = graph_digital(data)
    LHS = len(data)
    RHS = len(g) - 1 - LHS
    NIL = 0
    pair = [NIL] * (1 + LHS + RHS)
    dist = [math.inf] * (1 + LHS)

    def bfs():
        queue = []
        for i in range(1, LHS+1):
            if pair[i] == NIL:
                dist[i] = 0
                queue.append(i)
            else:
                dist[i] = math.inf

        dist[NIL] = math.inf
        while queue:
            vertex_lhs = queue.pop(0)
            if dist[vertex_lhs] < dist[NIL]:
                for neighbor in g[vertex_lhs]:
                    if math.isinf(dist[pair[neighbor]]):
                        dist[pair[neighbor]] = dist[vertex_lhs] + 1
                        queue.append(pair[neighbor])
        return math.isfinite(dist[NIL])

    def dfs(vertex_lhs: int):
        if vertex_lhs != NIL:
            for neighbor in g[vertex_lhs]:
                if dist[pair[neighbor]] == dist[vertex_lhs] + 1:
                    if dfs(pair[neighbor]):
                        pair[neighbor] = vertex_lhs
                        pair[vertex_lhs] = neighbor
                        return True
            dist[vertex_lhs] = math.inf
            return False
        return True

    no_of_matching = 0
    while bfs():
        for vertex_lhs in range(1, LHS+1):
            if pair[vertex_lhs] == NIL and dfs(vertex_lhs):
                no_of_matching += 1
    print(f"no of matching = {no_of_matching}")

    g_matching = dict()
    for i in range(1, LHS+1):
        g_matching[g_reverse[i]] = g_reverse[pair[i]]
    return g_matching

def part2(myticket: list[int], nearby: list[list[int]], fields: list[Field]):
    valid_tickets = [myticket]

    def ticket_is_valid(ticket: list[int]):
        for num in ticket:
            if num_is_invalid(num, fields):
                return False
        return True

    for ticket in nearby:
        if ticket_is_valid(ticket):
            valid_tickets.append(ticket)

    data = {i: set(x.name for x in fields) for i in range(1, len(valid_tickets[0])+1)}
    for i, s in enumerate(list(map(set, zip(*valid_tickets))), 1):
        for field in fields:
            # if not s.issubset(set(range(field.s1, field.e1+1)) | set(range(field.s2, field.e2+1))):
            #     data[i].remove(field.name)
            for num in s:
                if num < field.s1 or (num > field.e1 and num < field.s2) or num > field.e2:
                    data[i].remove(field.name)
                    break
    result = hopcroftkarp(data)
    print(f"matching = {result}")
    count = 1
    for k, v in result.items():
        if re.match(r"departure", v):
            count *= myticket[k-1]
    return count

if __name__ == "__main__":
    # fields, myticket, nearby = open_txt("test.txt")
    fields, myticket, nearby = open_txt("aoc16.txt")
    print("part 1: ", part1(nearby, fields))
    print("part 2: ", part2(myticket, nearby, fields))
