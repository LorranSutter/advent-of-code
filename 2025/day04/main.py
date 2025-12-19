import os
from typing import List, Tuple

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
To prepare the grid, we add a border of "." around the grid so we don't have to check for out-of-bounds indices

Part 1:
- We assume the total accessible rolls is equal to the product of rows and columns
- We descrease the total accessible rolls when we find a '.' or when we find a accessible roll
- Iterate over each cell in the grid
- If the cell is not a roll, go to the next cell
- If the cell is a roll, count the number of adjacent rolls that are "@"
- If the count is at least 4, remove the roll

Part 2:
- Similar to part 1, but instead of finding a roll that can't be removed, find a roll that can be removed
- Once we find a roll, just perform a flood fill in the adjacent cells untill no more rolls can be removed

Note:
It is implemented in a way we can choose the maximun adjanced rolls.
If we choose a number greater than 4, all rolls will be removed!
You can check that changing the max recursion depth

import sys
sys.setrecursionlimit(10000)

"""


@timer
def part1():
    rows, cols, rolls = parse_file()
    max_adj_rolls = 4
    directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    accessible_rolls = rows * cols
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if rolls[i][j] == ".":
                accessible_rolls -= 1
                continue

            adj_rolls = 0
            for d in directions:
                adj = (i + d[0], j + d[1])
                if rolls[adj[0]][adj[1]] == "@":
                    adj_rolls += 1
                    if adj_rolls >= max_adj_rolls:
                        accessible_rolls -= 1
                        break

    print("Total accessible rolls:", accessible_rolls)


@timer
def part2():
    rows, cols, rolls = parse_file()
    max_adj_rolls = 4

    for row in rolls:
        print("".join(row))

    removed_rolls = 0
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if rolls[i][j] == ".":
                continue

            removed_rolls = flood_fill(i, j, rolls, removed_rolls, max_adj_rolls)

    for row in rolls:
        print("".join(row))

    print("Total removed rolls:", removed_rolls)


def flood_fill(
    i: int, j: int, rolls: List[List[str]], removed_rolls: int, max_adj_rolls: int
) -> int:
    if rolls[i][j] == ".":
        return removed_rolls

    directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    adj_rolls = 0
    for d in directions:
        adj = (i + d[0], j + d[1])
        if rolls[adj[0]][adj[1]] == "@":
            adj_rolls += 1
            if adj_rolls >= max_adj_rolls:
                break

    if adj_rolls < max_adj_rolls:
        rolls[i][j] = "."
        removed_rolls += 1
        for d in directions:
            removed_rolls = flood_fill(
                i + d[0], j + d[1], rolls, removed_rolls, max_adj_rolls
            )

    return removed_rolls


def parse_file() -> Tuple[int, int, List[List[str]]]:
    rolls = []
    with open(abs_file_path) as f:
        for line in f:
            line = line.strip()
            line = ["."] + [i for i in line] + ["."]
            rolls.append(line)

    rows = len(rolls)
    cols = len(rolls[0])

    empty_row = ["."] * cols
    rolls.insert(0, empty_row)
    rolls.append(empty_row)

    return rows, cols - 2, rolls


part2()
