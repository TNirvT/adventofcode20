from copy import deepcopy
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

def bfs(data: dict, start: str) -> dict:
    lhs = set(data.keys())

    g = graph(data)
    visited = {x: False for x in g.keys()}
    queue = [start]
    visited[start] = True

    result = dict()

    while queue:
        vertex = queue.pop(0)
        for neighbor in g[vertex]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True

                if vertex in lhs and not result.get(vertex):
                    result[vertex] = neighbor
                elif vertex not in lhs and vertex not in result.values():
                    result[neighbor] = vertex
    return result

class Unmatched(NamedTuple):
    lhs: set
    rhs: set

def unmatched(data: dict, bfs_result: dict):
    lhs = set(data.keys())
    rhs = set()
    for neighbors in data.values():
        rhs |= set(neighbors)
    for k, v in bfs_result.items():
        lhs.remove(k)
        rhs.remove(v)
    return Unmatched(lhs, rhs)

def dfs(g: dict, start, ends: set) -> list:
    visited = set()
    visited.add(start)
    stack = [[start]]

    while stack:
        path = stack.pop()
        current = path[-1]
        if current in ends:
            return path

        for neighbor in g[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path_tmp = path[:]
                path_tmp.append(neighbor)
                stack.append(path_tmp)

    # raise ValueError("no path for this config")
    return []

def merge_dfs_path(bfs_result: dict, dfs_path: list):
    for i, vertex in enumerate(dfs_path):
        if i % 2:
            bfs_result[vertex] = dfs_path[i - 1]
    return bfs_result

if __name__ == "__main__":
    result = bfs(bipartite_data, "B")
    print(result)
    um = unmatched(bipartite_data, result)
    print(um)
    g = graph(bipartite_data)
    for vertex_r in um.rhs:
        path = dfs(g, vertex_r, um.lhs)
        print(f"path= {path}")
