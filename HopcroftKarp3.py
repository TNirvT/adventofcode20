from copy import deepcopy
import math

bipartite_data = {
    "B": [1, 4],
    "E": [7, 3, 6],
    "J": [2, 5, 4],
    "L": [7, 2],
    "T": [7, 6, 5],
    "A": [3, 6],
    "R": [6, 7]
}

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

# def graph_original(g_digital: dict, dict_revert: dict) -> dict:
#     g_original = dict()
#     for i, neighbors in enumerate(g_digital):
#         if i != 0:
#             g_original[dict_revert[i]] = [dict_revert[x] for x in neighbors]
#     return g_original

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
                print(pair)
    print(no_of_matching)

    g_matching = dict()
    for i in range(1, LHS+1):
        g_matching[g_reverse[i]] = g_reverse[pair[i]]
    return g_matching

if __name__ == "__main__":
    g_matching = hopcroftkarp(bipartite_data)
    print(g_matching)
