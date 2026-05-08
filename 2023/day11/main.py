import os
from typing import List, Tuple

from utils.timer import timer

"""
Explanation
"""


@timer
def part1():
    universe = parse_file("input.txt")

    expand_universe(universe, 1, True)
    print_universe(universe)

    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append((i, j))

    sum_shortest_paths = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            sum_shortest_paths += abs(galaxies[i][0] - galaxies[j][0]) + abs(
                galaxies[i][1] - galaxies[j][1]
            )

    print("Sum of shortest paths:", sum_shortest_paths)


@timer
def part2():
    pass


def expand_universe(
    universe: List[Tuple[str]], expansion_size: int, update_universe: bool = False
) -> Tuple[int, int]:
    rows_to_expand = []
    for i in range(len(universe)):
        if all(cell == "." for cell in universe[i]):
            if update_universe:
                rows_to_expand.append(i + len(rows_to_expand) * expansion_size)
            else:
                rows_to_expand.append(i)

    if update_universe:
        for i in rows_to_expand:
            for j in range(expansion_size):
                universe.insert(i+j, tuple("." for _ in range(len(universe[0]))))

    cols_to_expand = []
    for j in range(len(universe[0])):
        if all(universe[i][j] == "." for i in range(len(universe))):
            if update_universe:
                cols_to_expand.append(j + len(cols_to_expand) * expansion_size)
            else:
                cols_to_expand.append(j)

    if update_universe:
        for j in cols_to_expand:
            for k in range(expansion_size):
                for i in range(len(universe)):
                    universe[i] = universe[i][:j+k] + (".",) + universe[i][j+k:]

    return rows_to_expand, cols_to_expand



def print_universe(universe: List[Tuple[str]]):
    for row in universe:
        print("".join(row))


def parse_file(file_name: str) -> List[Tuple[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    universe = []
    with open(abs_file_path, "r") as f:
        for line in f:
            universe.append(tuple(cell for cell in line.strip()))
    return universe


part1()
# part2()