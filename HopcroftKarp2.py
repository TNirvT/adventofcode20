from copy import deepcopy
from random import randint
from typing import NamedTuple

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
        for i in v:
            if not g.get(i):
                g[i] = [k]
            else:
                g[i].append(k)
    return g

def graph_digital(data: dict) -> tuple[dict[int, list[int]], dict]:
    # all vertices are numbers(starts at 0), bi-directional
    dict_revert = {x: i for (i, x) in enumerate(data.keys())}
    rhs = set()
    for neighbors in data.values():
        rhs |= set(neighbors)

    if len(data) > len(rhs):
        print("number of vertices on LHS > RHS")
    elif len(data) < len(rhs):
        print("number of vertices on LHS < RHS")

    dict_revert.update({x: i for (i, x) in enumerate(rhs, len(data))})

    g_digital = dict()
    for k, v in graph(data).items():
        g_digital[dict_revert[k]] = [dict_revert[x] for x in v]

    return g_digital, dict(zip(dict_revert.values(), dict_revert.keys()))

def graph_original(g_digital: dict, dict_revert: dict) -> dict:
    g_original = dict()
    for k, v in g_digital:
        g_original[dict_revert[k]] = [dict_revert[x] for x in v]
    return g_original

def bfs(data: dict) -> dict: # the function is a reference / stepping-stone
    g, g_reverse = graph_digital(data)
    lhs = len(data)
    start = randint(0, lhs-1)
    # start = 0
    visited = {start}
    queue = [start]
    result = [None] * lhs
    results = []

    while queue:
        vertex = queue.pop(0)
        for neighbor in g[vertex]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

                if vertex in range(lhs) and result[vertex] is not None:
                    # vertex on LHS and unpaired
                    result[vertex] = neighbor
                elif vertex not in range(lhs) and vertex not in result:
                    # vertex on RHS and unpaired
                    result[neighbor] = vertex
    return {g_reverse[i]: g_reverse[x] for (i, x) in enumerate(result) if x is not None}

def bfs_allpaths(data: dict) -> list[list]:
    g, g_reverse = graph_digital(data)

    # create a dummy vertex NIL marking the end-point of all possible paths
    NIL = None
    # connect all vertices on the RHS to vertex NIL = None
    for i in range(len(data), len(g)):
        g[i].append(NIL)
    # there's no way out after reaching the end-point
    g[NIL] = []

    lhs = len(data)
    start = randint(0, lhs-1)
    # start = 0
    queue = [[start]]

    result = []
    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if (vertex == NIL):
            result.append({g_reverse[path[i]]: g_reverse[path[i+1]] for i in range(0, len(path)-1, 2)})

        for neighbor in g[vertex]:
            if neighbor not in path:
                newpath = deepcopy(path)
                newpath.append(neighbor)
                queue.append(newpath)

    return result

class Unpaired(NamedTuple):
    lhs: list
    rhs: list

def unpaired(data: dict, path: dict) -> Unpaired:
    lhs, rhs = [], []
    for vertex in data:
        if vertex not in path.keys():
            lhs.append(vertex)
    all_rhs = set()
    for neighbors in data.values():
        all_rhs |= set(neighbors)
    for vertex in all_rhs:
        if vertex not in path.values():
            rhs.append(vertex)
    return Unpaired(lhs, rhs)

def graph_dfs(data: dict, path: dict):
    free_vertices = unpaired(data, path)
    rhs = set()
    g_dfs = {vertex: data[vertex] for vertex in free_vertices.lhs}
    return

if __name__ == "__main__":
    paths = bfs_allpaths(bipartite_data)
    length = max(len(x) for x in paths)
    better_paths = [x for x in paths if len(x) == length]
    print(better_paths)
    free_vertices = unpaired(bipartite_data, better_paths[0])
    print(free_vertices)
