import os
import sys
from typing import List, Tuple

from utils.timer import timer

sys.setrecursionlimit(10**6)

"""
Preprocessing:
- Read the input file and parse it into 2D array of strings.
- Expand the boundaries of the grid with the character # to faciliatate findinding the borders.

Part 1:
- We made a function `cast_beam` to simulate the beam's movement that is pretty much a DFS approach.
- This function receives the current position along with the current direction of the beam.
- We perform a different recursive call depending on what the beam hits ('#', '|', '-', '.', '/', '\\').
- The trick here is to keep track of two sets:
  - `energized` to keep track of the positions we have already visited.
  - `mirrors_visited` to keep track of the mirrors we have already visited.
    - This is a set of pairs of (pos, dir) that says from which direction the beam came from.
    - This is highly important to avoid infinite loops.
- After finishing the recursive calls, we output the number of energized tiles.

Part 2:
- We can use the same function `cast_beam` from part 1.
- The difference is that we cast the beams from all spots on the borders.
- Keep track of the configuration with most energized tiles.
"""


@timer
def part1():
    grid = parse_file("input.txt")

    print("\nInitial grid")
    print_grid(grid)

    energized = set()
    # Start at (1, 1) to avoid the border
    cast_beam(grid, (1, 1), (0, 1), set(), energized)

    print("\nGrid after energizing tiles")
    print_grid(grid, energized)

    print(f"\nEnergized tiles:", len(energized))


@timer
def part2():
    grid = parse_file("input.txt")

    print("\nInitial grid")
    print_grid(grid)

    top = ((1, i) for i in range(1, len(grid[0]) - 1))
    bottom = ((len(grid[0]) - 2, pos[1]) for pos in top)
    left = ((i, 1) for i in range(1, len(grid) - 1))
    right = ((len(grid) - 2, pos[1]) for pos in left)

    edges = (top, bottom, left, right)
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    max_energized = set()
    for edge, direction in zip(edges, dirs):
        for pos in edge:
            energized = set()
            cast_beam(grid, pos, direction, set(), energized)

            if len(energized) > len(max_energized):
                max_energized = energized

    print("\nMost energized grid")
    print_grid(grid, max_energized)

    print(f"\nEnergized tiles:", len(max_energized))


def cast_beam(
    grid: List[Tuple[str]],
    pos: Tuple[int, int],
    dir: Tuple[int, int],
    mirrors_visited: set,
    energized: set,
):
    """
    Recursively simulates a light beam traveling through a grid with mirrors and splitters.

    The function traces the path of a light beam as it interacts with various elements:
    - Empty spaces ('.'): beam continues in the same direction
    - Borders ('#'): beam stops
    - Vertical splitters ('|'): splits beam up/down if traveling horizontally
    - Horizontal splitters ('-'): splits beam left/right if traveling vertically
    - Backslash mirrors ('\\'): reflects beam 90 degrees (row/col directions swap)
    - Forward slash mirrors ('/'): reflects beam 90 degrees (row/col directions swap)

    Args:
        grid (List[Tuple[str]]): A 2D grid represented as a list of tuples containing characters
            that represent the layout of mirrors, splitters, and boundaries.
        pos (Tuple[int, int]): The current position of the beam as (row, column) coordinates.
        dir (Tuple[int, int]): The direction vector of the beam as (row_delta, column_delta).
            For example, (0, 1) means moving right, (1, 0) means moving down.
        mirrors_visited (set): A set tracking visited mirror/splitter positions with their
            incoming directions as tuples of (position, direction) to prevent infinite loops.
        energized (set): A set of positions (row, column) that have been visited by the beam,
            representing energized tiles.

    Returns:
        None: The function modifies the `energized` and `mirrors_visited` sets in place.
    """
    if (pos, dir) in mirrors_visited:
        return

    energized.add(pos)

    match grid[pos[0]][pos[1]]:
        case "#":
            # Border: beam stops
            energized.remove(pos)
        case "|":
            # Vertical splitter: reflect beam 90 degrees both directions
            mirrors_visited.add((pos, dir))
            if dir == (0, 1) or dir == (0, -1):
                cast_beam(
                    grid,
                    (pos[0] - 1, pos[1]),
                    (-1, 0),
                    mirrors_visited,
                    energized,
                )
                cast_beam(
                    grid,
                    (pos[0] + 1, pos[1]),
                    (1, 0),
                    mirrors_visited,
                    energized,
                )
            else:
                # Beam continues in the same direction
                cast_beam(
                    grid,
                    (pos[0] + dir[0], pos[1] + dir[1]),
                    dir,
                    mirrors_visited,
                    energized,
                )
        case "-":
            # Horizontal splitter: reflect beam 90 degrees both directions
            mirrors_visited.add((pos, dir))
            if dir == (1, 0) or dir == (-1, 0):
                cast_beam(
                    grid,
                    (pos[0], pos[1] - 1),
                    (0, -1),
                    mirrors_visited,
                    energized,
                )
                cast_beam(
                    grid,
                    (pos[0], pos[1] + 1),
                    (0, 1),
                    mirrors_visited,
                    energized,
                )
            else:
                # Beam continues in the same direction
                cast_beam(
                    grid,
                    (pos[0] + dir[0], pos[1] + dir[1]),
                    dir,
                    mirrors_visited,
                    energized,
                )
        case "\\":
            # Slash mirror: reflect beam 90 degrees
            mirrors_visited.add((pos, dir))
            cast_beam(
                grid,
                (pos[0] + dir[1], pos[1] + dir[0]),
                (dir[1], dir[0]),
                mirrors_visited,
                energized,
            )
        case "/":
            # Slash mirror: reflect beam 90 degrees
            mirrors_visited.add((pos, dir))
            cast_beam(
                grid,
                (pos[0] - dir[1], pos[1] - dir[0]),
                (-dir[1], -dir[0]),
                mirrors_visited,
                energized,
            )
        case _:
            # Beam continues in the same direction
            cast_beam(
                grid,
                (pos[0] + dir[0], pos[1] + dir[1]),
                dir,
                mirrors_visited,
                energized,
            )


def print_grid(grid: List[Tuple[int, int]], energized: set = set()):
    for i in range(len(grid)):
        line = []
        for j in range(len(grid[i])):
            if (i, j) in energized and grid[i][j] == ".":
                line.append(" *")
            else:
                line.append(" " + grid[i][j])

        print("".join(line))


def parse_file(file_name: str) -> List[Tuple[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append(tuple(["#"] + [item for item in line.strip()] + ["#"]))

    grid.insert(0, tuple(["#"] * len(grid[0])))
    grid.append(tuple(["#"] * len(grid[0])))

    return grid


part1()
part2()
