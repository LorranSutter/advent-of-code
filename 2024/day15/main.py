import os
from typing import Tuple
from dataclasses import dataclass

from utils.timer import timer


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\x1b[6;30;42m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


@dataclass
class Node:
    symbol: str
    coord: Tuple[int]


script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    robot, grid, moves = read_file()

    for move in moves:
        robot = push_1(grid, robot, move, [robot])

    print_grid_1(grid)
    s = sum_gps_coordinates(grid)

    print("Sum of GPS coordinates:", s)


@timer
def part2():
    robot, grid, moves = read_file(True)

    for move in moves:
        path = push_2(grid, robot, move, [Node("@", robot)])

        if path != []:
            robot = add(path[0].coord, move)

            befores = []
            for item in path:
                if erase_before(grid, item, move, path):
                    befores.append(item.coord)
                new_pos = add(item.coord, move)
                grid[new_pos[0]][new_pos[1]] = item.symbol

            for before in befores:
                grid[before[0]][before[1]] = "."

    print_grid(grid, [])
    s = sum_gps_coordinates(grid)

    print("Sum of GPS coordinates:", s)


def read_file(remap=False):
    directions = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
    double = {"#": ("#", "#"), "O": ("[", "]"), ".": (".", "."), "@": ("@", ".")}
    robot, grid, moves = (), [], []

    with open(abs_file_path) as f:
        for i, line in enumerate(f):
            if line == "\n":
                break

            line = [p for p in line.rstrip("\n")]

            if not robot:
                for j in range(len(line)):
                    if line[j] == "@":
                        if remap:
                            j *= 2
                        robot = (i, j)
                        break

            if remap:
                new_line = []
                for item in line:
                    new_line.extend(double[item])
                grid.append(new_line)
            else:
                grid.append(line)

        for line in f:
            moves.extend([directions[m] for m in line.rstrip("\n")])

    return robot, grid, moves


def print_grid_1(grid):
    for i in range(len(grid)):
        print("".join(grid[i]))


def print_grid(grid, path):
    for i in range(len(grid)):
        line = ""
        for j in range(len(grid) * 2):
            if Node(grid[i][j], (i, j)) in path:
                line += f"{bcolors.OKGREEN}.{bcolors.ENDC}"
            else:
                line += grid[i][j]
        print(line)


def push_1(grid, p, d, path):
    next_symbol = grid[p[0] + d[0]][p[1] + d[1]]
    if next_symbol == "#":
        return path[0]
    elif next_symbol == "O":
        path.append(add(p, d))
        return push_1(grid, add(p, d), d, path)
    else:
        robot_old = path[0]
        robot_new = add(robot_old, d)
        grid[robot_old[0]][robot_old[1]] = "."
        grid[robot_new[0]][robot_new[1]] = "@"

        for box in path[1:]:
            grid[box[0] + d[0]][box[1] + d[1]] = "O"

        return robot_new


def push_2(grid, p, d, path):
    next_item = Node(grid[p[0] + d[0]][p[1] + d[1]], add(p, d))
    if next_item.symbol == "#":
        return []
    elif next_item.symbol in ("[", "]"):
        # Moving horizontally
        if d[0] == 0:
            path.append(next_item)
            return push_2(grid, next_item.coord, d, path)
        elif next_item.symbol == "[":
            if next_item not in path:
                path.append(next_item)
            box_pair = Node("]", add(next_item.coord, (0, 1)))
            if box_pair not in path:
                path.append(box_pair)
            path = push_2(grid, add(next_item.coord, (0, 1)), d, path)
            return [] if path == [] else push_2(grid, next_item.coord, d, path)
        else:  # "]"
            if next_item not in path:
                path.append(next_item)
            box_pair = Node("[", add(next_item.coord, (0, -1)))
            if box_pair not in path:
                path.append(box_pair)
            path = push_2(grid, add(next_item.coord, (0, -1)), d, path)
            return [] if path == [] else push_2(grid, next_item.coord, d, path)
    else:
        return path


def erase_before(grid, item, move, path):
    before = sub(item.coord, move)
    if grid[before[0]][before[1]] == "." or item.symbol == "@":
        return True
    for p in path:
        if before == p.coord:
            return False
    return True


def sum_gps_coordinates(grid):
    s = 0
    size = len(grid)
    for i in range(size):
        for j in range(len(grid[i])):
            if grid[i][j] in ("O", "["):
                s += 100 * i + j

    return s


def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])


part2()
