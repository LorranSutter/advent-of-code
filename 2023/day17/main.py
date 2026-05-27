import os
import math
import heapq
from typing import List, Tuple, Dict
from itertools import product
from enum import Enum

from utils.timer import timer
from utils.utils import print_grid, tcolors

"""
Preprocessing:
-

Part 1:
-

Part 2:
-
"""


# 971 too low
@timer
def part1():
    # TODO: Implement part 1
    city_map = parse_file("input_sample.txt")
    print_grid(city_map, "")

    start_pos = (1, 1)
    end_pos = (len(city_map) - 2, len(city_map[0]) - 2)
    d, min_path = dijkstra_1(city_map, start_pos, end_pos)
    print(f"Minimum distance: {d}, Path: {min_path}")

    for pos in min_path:
        city_map[pos[0]][
            pos[1]
        ] = f"{tcolors.GREEN}{str(city_map[pos[0]][pos[1]])}{tcolors.RESET}"

    print_grid(city_map, "")


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample.txt")
    pass


def print_with_path(grid: List[List[int]], path: List[Tuple[int]]):
    new_grid = [[str(cell) for cell in row] for row in grid]
    for pos in path:
        new_grid[pos[0]][
            pos[1]
        ] = f"{tcolors.GREEN}{str(new_grid[pos[0]][pos[1]])}{tcolors.RESET}"

    print_grid(new_grid, "")

class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Dist:
    def __init__(self, weight: int, dir: Direction, moves: int):
        self.weight = weight
        self.dir = dir
        self.moves = moves

    def __lt__(self, other):
        if other.moves > 3:
            return False
        return self.weight < other.weight
    
    def __str__(self):
        return f"Dist(weight={self.weight}, moves={self.moves})"

def dijkstra_1(
    grid: List[List[int]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:

    grid_len = len(grid) - 1

    # Priority queue
    pq = []
    dist = {coord: math.inf for coord in product(range(grid_len), range(grid_len))}
    parent = {coord: None for coord in product(range(grid_len), range(grid_len))}
    dist[start] = 0
    heapq.heappush(pq, (0, start))

    def reconstruct_path(end_node: Tuple[int]) -> List[Tuple[int]]:
        # Reconstruct path
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        # path.reverse()
        return d, path

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        d, u = heapq.heappop(pq)

        if u == end:
            return reconstruct_path(u)

        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue

        for dir in dirs:
            v = (u[0] + dir[0], u[1] + dir[1])
            w = grid[v[0]][v[1]]
            if w == 0:
                continue

            # if priority(u, w) < dist[v]:
            if dist[u] + w < dist[v]:
                print(f"Recalculating {u} -> {v} with weight {w}")

                # _, path = reconstruct_path(u)
                # print_with_path(grid, path)
                dist[v] = dist[u] + w
    
                # moves[v] = moves[u] + 1
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return -1, []

def dijkstra(
    grid: List[List[int]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:

    grid_len = len(grid) - 1

    # Priority queue
    pq = []
    dist = {
        coord: Dist(math.inf, Direction.HORIZONTAL ,1) for coord in product(range(grid_len), range(grid_len))
    }
    moves = {
        coord: ((0, 0), (0, 0)) for coord in product(range(grid_len), range(grid_len))
    }
    parent = {coord: None for coord in product(range(grid_len), range(grid_len))}
    dist[start] = Dist(0, Direction.VERTICAL, 1)
    heapq.heappush(pq, (dist[start], start))

    def priority(coord: Tuple[int], weight: int) -> int:
        h, v = 0, 0

        curr = coord
        p = parent[curr]
        while p is not None:
            if p[0] == curr[0]:
                if v > 0:
                    break
                h += 1
                if h > 7:
                    return math.inf
            else:
                if h > 0:
                    break
                v += 1
                if v > 7:
                    return math.inf
            curr = p
            p = parent[p]

        return dist[coord] + weight

    def reconstruct_path(end_node: Tuple[int]) -> List[Tuple[int]]:
        # Reconstruct path
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        # path.reverse()
        return d, path

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        d, u = heapq.heappop(pq)

        if u == end:
            return reconstruct_path(u)

        # If this distance not the latest shortest one, skip it
        if d.weight > dist[u].weight:
            continue

        for dir in dirs:
            v = (u[0] + dir[0], u[1] + dir[1])
            w = grid[v[0]][v[1]]
            if w == 0:
                continue

            # if priority(u, w) < dist[v]:
            if dist[u].weight + w < dist[v].weight:
                print(f"Recalculating {u} -> {v} with weight {w}")

                if dist[u].moves > 2:
                    # Vertical move
                    if u[0] == v[0] and dist[u].dir == Direction.VERTICAL:
                        continue
                    # Horizontal move
                    elif u[1] == v[1] and dist[u].dir == Direction.HORIZONTAL:
                        continue

                # _, path = reconstruct_path(u)
                # print_with_path(grid, path)

                if u[0] == v[0] and dist[u].dir == Direction.VERTICAL:
                    dist[v] = Dist(dist[u].weight + w, dist[u].dir, dist[u].moves + 1)
                elif u[1] == v[1] and dist[u].dir == Direction.HORIZONTAL:
                    dist[v] = Dist(dist[u].weight + w, dist[u].dir, dist[u].moves + 1)
                elif dist[u].dir == Direction.VERTICAL:
                    dist[v] = Dist(dist[u].weight + w, Direction.HORIZONTAL, 1)
                else:
                    dist[v] = Dist(dist[u].weight + w, Direction.VERTICAL, 1)
    
                # moves[v] = moves[u] + 1
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return -1, []


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    city_map = []
    with open(abs_file_path, "r") as f:
        for line in f:
            city_map.append([0] + [int(cell) for cell in line.strip()] + [0])

    city_map.insert(0, [0] * len(city_map[0]))
    city_map.append([0] * len(city_map[0]))

    return city_map


part1()
# part2()
