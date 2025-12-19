import os
import math
import collections
from dataclasses import dataclass

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input_sample"
abs_file_path = os.path.join(script_dir, rel_path)


@dataclass
class Node:
    weight: int
    vertex: tuple


@timer
def part1():
    grid, path, start, end = read_file()
    print(path)
    print(start)
    print(end)

    print_grid(grid)

    adjacent_matrix = make_adjacent_matrix_3(grid, path)

    for key in adjacent_matrix.keys():
        print(key, adjacent_matrix[key])

    # _, parents = BFS(adjacent_matrix, {"weight": 0, "vertex": start}, end)

    # v = end
    # while True:
    #     if v == start:
    #         break
    #     print(v)
    #     v = parents[v]

    dist, prev = Dijkstra(adjacent_matrix, path, start)

    print("out")
    print(dist)
    print(prev)

    v = {"weight": 0, "vertex": end}
    s = 0
    count = 0
    while True:
        count += 1
        s += v["weight"]
        if v["vertex"] == start:
            break
        print(v)
        v = prev[v["vertex"]]

    print("Lowest score:", s, count)


@timer
def part2():

    print("Sum of GPS coordinates:")


def read_file():
    start, end = (), ()
    grid, path = [], []
    with open(abs_file_path) as f:
        for i, line in enumerate(f):
            grid.append(
                [item if item not in ("S", "E") else "." for item in line.rstrip("\n")]
            )
            for j, item in enumerate(line.rstrip("\n")):
                if item == "#":
                    continue
                path.append((i, j))
                if item == "S":
                    start = (i, j)
                elif item == "E":
                    end = (i, j)

    return grid, path, start, end


def make_adjacent_matrix(grid, path):
    adjacent_matrix = {}

    for p in path:
        adjacent_matrix[p] = []
        if grid[p[0] + 1][p[1]] == ".":
            adjacent_matrix[p].append((p[0] + 1, p[1]))
        if grid[p[0] - 1][p[1]] == ".":
            adjacent_matrix[p].append((p[0] - 1, p[1]))
        if grid[p[0]][p[1] + 1] == ".":
            adjacent_matrix[p].append((p[0], p[1] + 1))
        if grid[p[0]][p[1] - 1] == ".":
            adjacent_matrix[p].append((p[0], p[1] - 1))

    return adjacent_matrix


def make_adjacent_matrix_3(grid, path):
    adjacent_matrix = {}

    up = lambda p: grid[p[0] - 1][p[1]]
    down = lambda p: grid[p[0] + 1][p[1]]
    right = lambda p: grid[p[0]][p[1] + 1]
    left = lambda p: grid[p[0]][p[1] - 1]

    for p in path:
        adjacent_matrix[p] = []
        if down(p) == ".":
            if right(p) == "#" and left(p) == "#":
                adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] + 1, p[1])})
            else:
                if right(p) == "#" and up(p) == "#" and left(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] + 1, p[1])}
                    )
                elif left(p) == "#" and up(p) == "#" and right(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] + 1, p[1])}
                    )
                else:
                    adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] + 1, p[1])})
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] + 1, p[1])}
                    )
        if up(p) == ".":
            if right(p) == "#" and left(p) == "#":
                adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] - 1, p[1])})
            else:
                if right(p) == "#" and down(p) == "#" and left(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] - 1, p[1])}
                    )
                elif left(p) == "#" and down(p) == "#" and right(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] - 1, p[1])}
                    )
                else:
                    adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] - 1, p[1])})
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0] - 1, p[1])}
                    )
        if right(p) == ".":
            if down(p) == "#" and up(p) == "#":
                adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] + 1)})
            else:
                if down(p) == "#" and left(p) == "#" and up(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] + 1)}
                    )
                elif up(p) == "#" and left(p) == "#" and down(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] + 1)}
                    )
                else:
                    adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] + 1)})
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] + 1)}
                    )
        if left(p) == ".":
            if down(p) == "#" and up(p) == "#":
                adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] - 1)})
            else:
                if down(p) == "#" and right(p) == "#" and up(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] - 1)}
                    )
                elif up(p) == "#" and right(p) == "#" and down(p) == ".":
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] - 1)}
                    )
                else:
                    adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] - 1)})
                    adjacent_matrix[p].append(
                        {"weight": 1000, "vertex": (p[0], p[1] - 1)}
                    )

    return adjacent_matrix


def make_adjacent_matrix_2(grid, path):
    adjacent_matrix = {}

    for p in path:
        adjacent_matrix[p] = []
        if grid[p[0] + 1][p[1]] == ".":
            adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] + 1, p[1])})
            adjacent_matrix[p].append({"weight": 1000, "vertex": (p[0] + 1, p[1])})
        if grid[p[0] - 1][p[1]] == ".":
            adjacent_matrix[p].append({"weight": 1, "vertex": (p[0] - 1, p[1])})
            adjacent_matrix[p].append({"weight": 1000, "vertex": (p[0] - 1, p[1])})
        if grid[p[0]][p[1] + 1] == ".":
            adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] + 1)})
            adjacent_matrix[p].append({"weight": 1000, "vertex": (p[0], p[1] + 1)})
        if grid[p[0]][p[1] - 1] == ".":
            adjacent_matrix[p].append({"weight": 1, "vertex": (p[0], p[1] - 1)})
            adjacent_matrix[p].append({"weight": 1000, "vertex": (p[0], p[1] - 1)})

    return adjacent_matrix


def BFS(adjacent_matrix, start, end):
    Q, visited = [], []
    visited.append(start)
    Q.append(start)
    parents = {}
    while Q != []:
        v = Q.pop(0)
        if v == end:
            return v, parents
        for w in adjacent_matrix[v["vertex"]]:
            if w not in visited:
                visited.append(w)
                parents[w["vertex"]] = v
                Q.append(w)
    return None, None


def Dijkstra(adjacent_matrix, path, start):
    dist = collections.defaultdict(lambda: math.inf)
    prev = collections.defaultdict(lambda: None)
    # Q = []
    for p in path:
        dist[p] = math.inf
        # Q.append(p)

    dist[start] = 0

    while path != []:
        u = get_vertex_with_min_dist(path, dist)
        print(u)
        print(path)
        path.remove(u)

        for v in adjacent_matrix[u]:
            print(u, adjacent_matrix[u])
            print("here1")
            if v["vertex"] in path:
                print("here2")
                alt = dist[u] + v["weight"]
                if alt < dist[v["vertex"]]:
                    dist[v["vertex"]] = alt
                    prev[v["vertex"]] = {"weight": v["weight"], "vertex": u}

    return dist, prev


def get_vertex_with_min_dist(Q, dist):
    min_dist = math.inf
    vertex = None
    for v in Q:
        if dist[v] < min_dist:
            min_dist = dist[v]
            vertex = v
    return vertex


def print_grid(grid):
    for i in range(len(grid)):
        print("".join(grid[i]))


part1()
