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
    universe = parse_file("input_sample.txt")
    expansion_size = 10

    row_expansions, col_expansions = expand_universe(universe, expansion_size, True)
    print(row_expansions, col_expansions)

    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append((i, j))
    
    print_universe(universe)
    
    sum_shortest_paths = 0
    count_row_expanded_galaxies = 0
    count_col_expanded_galaxies = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            rows_between, cols_between = get_expansions_between_galaxies(galaxies[i], galaxies[j], row_expansions, col_expansions)
            # print(f"Expansions {galaxies[i]} and {galaxies[j]}: {rows_between} {cols_between}")

            if len(rows_between) > 0:
                count_row_expanded_galaxies += 1
            if len(cols_between) > 0:
                count_col_expanded_galaxies += 1
            
            # x_path = abs(galaxies[i][0] - galaxies[j][0]) + len(rows_between) * (expansion_size-1)
            # y_path = abs(galaxies[i][1] - galaxies[j][1]) + len(cols_between) * (expansion_size-1)

            # print(f"Path between {galaxies[i]} and {galaxies[j]}: x_path={x_path}, y_path={y_path}")

            # sum_shortest_paths += x_path + y_path

            path = abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
            print(f"Expansions {str(galaxies[i]):9} and {str(galaxies[j]):9}: {str(rows_between):8} {str(cols_between):12}, path={path}")
            sum_shortest_paths += path

    print(f"Count total row expanded galaxies: {count_row_expanded_galaxies}")
    print(f"Count total column expanded galaxies: {count_col_expanded_galaxies}")
    print(f"Count total expanded galaxies: {count_row_expanded_galaxies + count_col_expanded_galaxies}")
    print("Sum of shortest paths:", sum_shortest_paths)


def expand_universe(
    universe: List[Tuple[str]], expansion_size: int, update_universe: bool = False
) -> Tuple[int, int]:
    if expansion_size <= 1:
        return [], []
    
    rows_to_expand = []
    for i in range(len(universe)):
        if all(cell == "." for cell in universe[i]):
            if update_universe:
                rows_to_expand.append(i + len(rows_to_expand) * (expansion_size - 1))
            else:
                rows_to_expand.append(i)

    if update_universe:
        for i in rows_to_expand:
            for j in range(expansion_size-1):
                universe.insert(i+j, tuple("." for _ in range(len(universe[0]))))

    cols_to_expand = []
    for j in range(len(universe[0])):
        if all(universe[i][j] == "." for i in range(len(universe))):
            if update_universe:
                cols_to_expand.append(j + len(cols_to_expand) * (expansion_size - 1))
            else:
                cols_to_expand.append(j)

    if update_universe:
        for j in cols_to_expand:
            for k in range(expansion_size-1):
                for i in range(len(universe)):
                    universe[i] = universe[i][:j+k] + (".",) + universe[i][j+k:]

    return rows_to_expand, cols_to_expand


def get_expansions_between_galaxies(
    galaxy1: Tuple[int, int],
    galaxy2: Tuple[int, int],
    row_expansions: List[int],
    col_expansions: List[int],
) -> Tuple[List[int], List[int]]:
    x1, x2 = sorted([galaxy1[0], galaxy2[0]])
    y1, y2 = sorted([galaxy1[1], galaxy2[1]])

    rows_between = []
    for row in row_expansions:
        if x1 < row < x2:
            rows_between.append(row)
    
    cols_between = []
    for col in col_expansions:
        if y1 < col < y2:
            cols_between.append(col)
    
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


# part1()
part2()


# .....#..........
# ...........#....
# #...............
# ................
# ................
# ................
# ..........#.....
# .#..............
# ...............#
# ................
# ................
# ................
# ...........#....
# #.....#.........

# 2 5 8
# ....#.......
# .........#..
# #...........
# ............
# ........#...
# .#..........
# ...........#
# ............
# .........#..
# #....#......

# .....#..........
# ...........#....
# #...............
# ................
# ................
# ................
# ..........#.....
# .#..............
# ...............#
# ................
# ................
# ................
# ...........#....
# #.....#.........

# .....#..........
# .............#..
# #...............
# ................
# ................
# ................
# ............#...
# .#..............
# ................
# ................
# ...............#
# ................
# .............#..
# #.......#.......