import os
from typing import List, Tuple, Dict
from collections import defaultdict

from utils.timer import timer

"""
Preprocessing:
- Read the 2D engine schematic grid from the input file
- Pad the grid with an extra border of periods (`.`) on all sides (top, bottom, left, and right)
  to make neighborhood checks simpler and avoid index out of bounds errors

Part 1:
- Scan each line of the grid to identify consecutive digits that form numbers
- For each number found, check all 8-way neighboring cells surrounding the characters of the number
- If at least one neighboring cell contains a symbol (any character other than a digit or `.`), classify it as a valid part number
- Sum all valid part numbers and print the total

Part 2:
- Scan the schematic grid to find numbers in the same manner as Part 1
- For each number, check if any adjacent neighboring cell is a gear symbol (`*`)
- Keep a dictionary mapping each gear's coordinate `(row, col)` to a list of adjacent part numbers
- After scanning, find all gears that are adjacent to exactly two part numbers
- Multiply those two numbers to get the gear ratio, sum all gear ratios, and print the total
"""

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    grid = read_file()
    n, m = len(grid), len(grid[0])
    nums = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    sum_nums = 0

    for i in range(1, n - 1):
        startNum = -1
        for j in range(1, m):
            if grid[i][j] in nums:
                if startNum == -1:
                    startNum = j
            elif startNum > -1:
                if is_adjacent_to_symbol(grid, i, startNum, j):
                    sum_nums += int("".join(grid[i][startNum:j]))
                startNum = -1

    print("Sum of adjacent numbers:", sum_nums)


@timer
def part2():
    grid = read_file()
    n, m = len(grid), len(grid[0])
    nums = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    # Maps gear position to list of numbers
    gear_map = defaultdict(list)

    for i in range(1, n - 1):
        startNum = -1
        for j in range(1, m):
            if grid[i][j] in nums:
                if startNum == -1:
                    startNum = j
            elif startNum > -1:
                update_adjacent_gear(grid, gear_map, i, startNum, j)
                startNum = -1

    sum_gear_ratios = 0
    for gear_pos in gear_map:
        if len(gear_map[gear_pos]) == 2:
            sum_gear_ratios += gear_map[gear_pos][0] * gear_map[gear_pos][1]

    print("Sum all gear ratios:", sum_gear_ratios)


def is_adjacent_to_symbol(
    grid: List[List[str]], line: int, start: int, end: int
) -> bool:
    not_symbol = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])

    # Horizontal boundaries
    if grid[line][start - 1] not in not_symbol:
        return True
    if grid[line][end] not in not_symbol:
        return True

    # Vertical boundaries
    for j in range(start - 1, end + 1):
        if grid[line - 1][j] not in not_symbol:
            return True
        if grid[line + 1][j] not in not_symbol:
            return True

    return False


def update_adjacent_gear(
    grid: List[List[str]],
    gear_dict: Dict[Tuple[int], List[int]],
    line: int,
    start: int,
    end: int,
):
    number = int("".join(grid[line][start:end]))

    # Horizontal boundaries
    if grid[line][start - 1] == "*":
        gear_dict[tuple([line, start - 1])].append(number)
    if grid[line][end] == "*":
        gear_dict[tuple([line, end])].append(number)

    # Vertical boundaries
    for j in range(start - 1, end + 1):
        if grid[line - 1][j] == "*":
            gear_dict[tuple([line - 1, j])].append(number)
        if grid[line + 1][j] == "*":
            gear_dict[tuple([line + 1, j])].append(number)


def read_file() -> List[List[str]]:
    grid = []
    with open(abs_file_path) as f:
        for line in f:
            line = line.rstrip("\n")
            # Add extra space on the sides
            grid.append(["."] + [item for item in line] + ["."])

    # Add extra line at the beginning and at the end
    extra_line = ["."] * len(grid[0])
    grid.insert(0, extra_line)
    grid.append(extra_line)

    return grid


part1()
part2()
