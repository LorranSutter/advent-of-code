import os
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Just read the input file and parse into a 2D list

Part 1:
- The trick here is to realize that the shortest path between two galaxies is just the Manhattan distance:
    - Euclidian distance: sqrt((x2-x1)^2 + (y2-y1)^2)
    - Manhattan distance: abs(x2-x1) + abs(y2-y1)
- I used the naive approach to expand the universe by adding more rows and columns of empty cells (function expand_universe)
- Finally, we just have to iterate over each pair of galaxies, calculate the Manhattan distance and add it to the total

Part 2:
- The part 2 was quite predictable, same idea as part 1, but with a way larger expanded universe
- The "aha moment" here is to realize the universe expansion is pretty much a linear transformation
- So, if we know how much the universe expanded, we can perform the same process of part 1 plus the expansion size
- We changed the "expande_universe" function
    - Accepts the size of the expansion and return which rows and columns were expanded
    - Not changing the universe matrix itself, so we can expanded how much we want without worrying about the memory usage
- Then, we iterate over each pair of galaxies, get how many rows and columns were between each pair with the function "get_expansions_between_galaxies"
- Finally, we calculate the Manhattan distance with the offset of the expansion:
    - x_path = abs(x2-x1) + num_rows + expansion_size
    - y_path = abs(y2-y1) + num_cols + expansion_size
    - total += x_path + y_path
"""


@timer
def part1():
    universe = parse_file("input.txt")

    expand_universe(universe, 2, True)
    print_universe(universe)

    galaxies = get_list_of_galaxies(universe)

    sum_shortest_paths = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            x_path = abs(galaxies[i][0] - galaxies[j][0])
            y_path = abs(galaxies[i][1] - galaxies[j][1])

            sum_shortest_paths += x_path + y_path

    print("Sum of shortest paths:", sum_shortest_paths)


@timer
def part2():
    universe = parse_file("input.txt")
    expansion_size = 1000000

    row_expansions, col_expansions = expand_universe(universe, expansion_size, False)
    galaxies = get_list_of_galaxies(universe)

    print_universe(universe)

    expansion_size -= 1
    sum_shortest_paths = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            num_rows, num_cols = get_expansions_between_galaxies(
                galaxies[i], galaxies[j], row_expansions, col_expansions
            )

            x_path = abs(galaxies[i][0] - galaxies[j][0]) + num_rows * expansion_size
            y_path = abs(galaxies[i][1] - galaxies[j][1]) + num_cols * expansion_size

            sum_shortest_paths += x_path + y_path

    print("Sum of shortest paths:", sum_shortest_paths)


def expand_universe(
    universe: List[Tuple[str]], expansion_size: int, update_universe: bool = False
) -> Tuple[int, int]:
    """
    Calculate the universe expanded by the given expansion size.
    If update_universe is True, the universe will be updated with the new rows and columns.
    """
    if expansion_size <= 1:
        return [], []
    expansion_size -= 1

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
                universe.insert(i + j, tuple("." for _ in range(len(universe[0]))))

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
                    universe[i] = universe[i][: j + k] + (".",) + universe[i][j + k :]

    return rows_to_expand, cols_to_expand


def get_list_of_galaxies(universe: List[Tuple[str]]) -> List[Tuple[int, int]]:
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append((i, j))
    return galaxies


def get_expansions_between_galaxies(
    galaxy1: Tuple[int, int],
    galaxy2: Tuple[int, int],
    row_expansions: List[int],
    col_expansions: List[int],
) -> Tuple[int, int]:
    """
    Returns the lists of rows and columns that are expandable between two galaxies
    """
    x1, x2 = sorted([galaxy1[0], galaxy2[0]])
    y1, y2 = sorted([galaxy1[1], galaxy2[1]])

    rows_between = 0
    for row in row_expansions:
        if x1 < row < x2:
            rows_between += 1

    cols_between = 0
    for col in col_expansions:
        if y1 < col < y2:
            cols_between += 1

    return rows_between, cols_between


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
part2()
