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

def bfs_allpaths(data: dict) -> list[dict]:
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

def graph_dfs(data: dict, bfs_path: dict):
    free_vertices = unpaired(data, bfs_path)
    g_dfs = dict()
    count_down = len(free_vertices.rhs)
    bfs_dict = dict(zip(bfs_path.values(), bfs_path.keys()))
    alt_layer = set()
    while count_down > 0:
        if not alt_layer:
            layer = free_vertices.lhs
        else:
            layer = set()
            for vertex in alt_layer:
                g_dfs[bfs_dict[vertex]] = [vertex]
                layer.add(bfs_dict[vertex])
            alt_layer = set()
        for vertex in layer:
            for neighbor in data[vertex]:
                if neighbor in g_dfs.keys():
                    g_dfs[neighbor].append(vertex)
                else:
                    g_dfs[neighbor] = [vertex]
                if neighbor in free_vertices.rhs:
                    count_down -= 1
                alt_layer.add(neighbor)
    return g_dfs

    # result = deepcopy(bfs_path)
    # for start in free_vertices.lhs:
    #     stack = [[start]]
    #     while stack:
    #         path = stack.pop()
    #         current = path[-1]
    #         if current in free_vertices.rhs:
    #             free_vertices.lhs.remove(start)
    #             free_vertices.rhs.remove(current)
    #             for i in range(len(path)):
    #                 if not i % 2:
    #                     result[path[i+1]] = path[i]
    #             break
            
    # return

if __name__ == "__main__":
    paths = bfs_allpaths(bipartite_data)
    length = max(len(x) for x in paths)
    better_paths = [x for x in paths if len(x) == length]
    print(better_paths[0])
    g_dfs = graph_dfs(bipartite_data, better_paths[0])
    print(g_dfs)
