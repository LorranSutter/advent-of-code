import os

from typing import List, Tuple
from shapely.geometry import Polygon, Point
from dataclasses import dataclass

from utils.timer import timer
from utils.utils import print_grid, tcolors

"""
Preprocessing:
- Read the input file and parse it into a 2D matrix of strings.
- Add boundary characters ('#') around the entire grid to simplify boundary checking in subsequent steps.

Part 1:
- Created a `Pipe` class that stores references to the two adjacent pipes connected to the current one.
- Converted the 2D matrix into a unidimensional array of `Pipe` objects, where each pipe stores indices 
  pointing to its connected neighbors in the array.
- Starting from point S, initialized two pointers that traverse the pipe loop in opposite directions simultaneously.
- When the two pointers meet, that position represents the farthest point from the start.
- Counted the steps taken during each iteration to determine the distance.

Alternative approach: Calculate the total length of the pipe loop and divide by 2.

Example:
  For the square loop:
  .....
  .S-7.
  .|.|.
  .L-J.
  .....
  
  The two pointers start at S and move in opposite directions:
  - Pointer 1: S → - → 7 → | → J → ...
  - Pointer 2: S → | → L → - → J → ...
  They meet at the farthest point after 4 steps.

Part 2:
- The goal is to count tiles enclosed within the main pipe loop.
- This involves multiple steps (kept separate for readability, though they could be combined):

  1. Find starting point: Scan the matrix to locate the starting position S.

  2. Extract pipe loop path: Traverse from S to find all coordinates (x, y) that belong to the main pipe loop.
     Return this as a list of coordinates.
  
  3. Create polygon geometry: Use the Shapely library to create a `Polygon` from the pipe loop coordinates.
     This polygon will be used to determine if points are inside or outside the loop.
  
  4. Remove disconnected pipes: Some inputs contain pipes not connected to the main loop.
     Mark these as ground ('.') using Shapely's `touches()` function to check if a point is part of the main loop.
  
  5. Flood fill to count enclosed tiles: 
     - Iterate over each pipe in the main loop.
     - For each pipe, examine adjacent ground tiles ('.').
     - For unvisited adjacent ground, use Shapely's `contains()` to determine if it's inside or outside the loop.
     - Apply Flood Fill (BFS) starting from that ground tile:
       - Mark inner tiles as 'I' (green)
       - Mark outer tiles as 'O' (blue)
     - Skip flood fill if an adjacent tile is already marked or is a boundary ('#').
     - The `flood_fill()` function returns the count of tiles filled, allowing us to track inner tile totals.

Example visualization:
  Before flood fill:
  #############
  #...........#
  #.S-------7.#
  #.|F-----7|.#
  #.||.....||.#
  #.||.....||.#
  #.|L-7.F-J|.#
  #.|..|.|..|.#
  #.L--J.L--J.#
  #...........#
  #############

  After flood fill:
  #############
  #OOOOOOOOOOO#
  #OS-------7O#
  #O|F-----7|O#
  #O||OOOOO||O#
  #O||OOOOO||O#
  #O|L-7OF-J|O#
  #O|II|O|II|O#
  #OL--JOL--JO#
  #OOOOOOOOOOO#
  
  Inner tiles (I): 4
  Outer tiles (O): remaining ground tiles
"""


@dataclass
class Pipe:
    Left: int
    Right: int


@dataclass
class Coord:
    X: int
    Y: int


script_dir = os.path.dirname(__file__)
rel_path = "input_sample_4.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    matrix = read_file()
    start, pipes = parse_matrix_to_pipes(matrix)

    previous_left, left = start[0], start[1].Left
    previous_right, right = start[0], start[1].Right
    steps = 0
    while True:
        steps += 1

        # Found farthest point
        if left == right:
            break

        # Make sure to not return back to the same pipe
        if previous_left != pipes[left].Left:
            previous_left = left
            left = pipes[left].Left
        else:
            previous_left = left
            left = pipes[left].Right

        # Make sure to not return back to the same pipe
        if previous_right != pipes[right].Right:
            previous_right = right
            right = pipes[right].Right
        else:
            previous_right = right
            right = pipes[right].Left

    print("Steps to farthest point:", steps)


@timer
def part2():

    matrix = read_file()

    start = find_start(matrix)
    pipes_path = find_pipes_path(start, matrix)

    # Build the polygon of the pipes path to check if a point is inside or outside of it
    poly = Polygon([(pipe.X, pipe.Y) for pipe in pipes_path])

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != "#" and not poly.touches(Point(i, j)):
                matrix[i][j] = "."

    inner_tile_count, outer_tile_count = 0, 0

    inner_tile = f"{tcolors.GREEN}I{tcolors.RESET}"
    outer_tile = f"{tcolors.BLUE}O{tcolors.RESET}"

    for pipe in pipes_path:
        adj_grounds = get_adjacent_ground(matrix, pipe.X, pipe.Y)
        for point in adj_grounds:
            # Boundary or already visited
            if matrix[point.X][point.Y] in ["#", outer_tile, inner_tile]:
                continue
            if poly.contains(Point(point.X, point.Y)):
                inner_tile_count += flood_fill(matrix, point, inner_tile)
            else:
                outer_tile_count += flood_fill(matrix, point, outer_tile)

    print_grid(matrix)
    print(f"Total tiles enclosed by the loop: {inner_tile_count}")
    print(f"Total tiles outside the loop: {outer_tile_count}")


def parse_matrix_to_pipes(matrix: List[Tuple[str]]) -> Tuple[Pipe, List[Pipe]]:
    """
    Converts the 2-dim to a unidimensional array
    Each array element is a Pipe(left, right), where
    left and right points to the array index of the adjacent pipe
    """
    m, n = len(matrix), len(matrix[0])

    start = Tuple[int, Pipe]
    pipes = list()

    for i in range(m):
        for j in range(n):
            match matrix[i][j]:
                case "|":
                    pipe = Pipe((i - 1) * n + j, (i + 1) * n + j)
                case "-":
                    pipe = Pipe(i * n + j - 1, i * n + j + 1)
                case "L":
                    pipe = Pipe((i - 1) * n + j, i * n + j + 1)
                case "J":
                    pipe = Pipe((i - 1) * n + j, i * n + j - 1)
                case "7":
                    pipe = Pipe(i * n + j - 1, (i + 1) * n + j)
                case "F":
                    pipe = Pipe(i * n + j + 1, (i + 1) * n + j)
                case "S":
                    start = (
                        i * n + j,
                        Pipe(*get_start_pipe_boundaries(matrix, i, j, True)),
                    )
                case _:
                    # We have to append non-pipes to make the unidimensional matrix work
                    pipe = Pipe(-1, -1)
            pipes.append(pipe)

    return start, pipes


def find_start(matrix: List[List[str]]) -> Coord:
    """Finds the coordinates of the starting point S"""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "S":
                return Coord(i, j)


def find_pipes_path(start: Coord, matrix: List[List[str]]) -> List[Coord]:
    """Finds the path of the pipes starting from S until it finds S again"""
    _, next_pipe = get_start_pipe_boundaries(matrix, start.X, start.Y)

    previous, left, right = start, None, None
    pipe_path = list()
    while True:
        pipe_path.append(previous)
        # Got back to the starting point
        if next_pipe == start:
            break

        match matrix[next_pipe.X][next_pipe.Y]:
            case "|":
                left = Coord(next_pipe.X - 1, next_pipe.Y)
                right = Coord(next_pipe.X + 1, next_pipe.Y)
            case "-":
                left = Coord(next_pipe.X, next_pipe.Y - 1)
                right = Coord(next_pipe.X, next_pipe.Y + 1)
            case "L":
                left = Coord(next_pipe.X - 1, next_pipe.Y)
                right = Coord(next_pipe.X, next_pipe.Y + 1)
            case "J":
                left = Coord(next_pipe.X - 1, next_pipe.Y)
                right = Coord(next_pipe.X, next_pipe.Y - 1)
            case "7":
                left = Coord(next_pipe.X, next_pipe.Y - 1)
                right = Coord(next_pipe.X + 1, next_pipe.Y)
            case "F":
                left = Coord(next_pipe.X, next_pipe.Y + 1)
                right = Coord(next_pipe.X + 1, next_pipe.Y)

        # Make sure to not return back to the same pipe
        if previous != left:
            previous = next_pipe
            next_pipe = left
        else:
            previous = next_pipe
            next_pipe = right

    return pipe_path


def get_start_pipe_boundaries(
    matrix: List[Tuple[str]], i: int, j: int, unidim: bool = False
) -> List[Coord | int]:
    """
    Returns the coordinates of the adjacent pipes to the starting point S

    Arguments:
        matrix: 2D matrix representing the tiles
        i: row index of the starting point S
        j: column index of the starting point S
        unidim: whether to return unidimensional indices

    Returns:
        List[Coord | int]: coordinates of the adjacent pipes
    """
    m, n = len(matrix), len(matrix[0])
    pipe_boundaries = list()

    # Only consider pipes that connects to S
    # In the following case, F is not connected
    # . | .
    # . S F
    # . J .
    if i > 0 and matrix[i - 1][j] in ("|", "7", "F"):
        pipe_boundaries.append((i - 1) * n + j if unidim else Coord(i - 1, j))
    if i < m - 1 and matrix[i + 1][j] in ("|", "L", "J"):
        pipe_boundaries.append((i + 1) * n + j if unidim else Coord(i + 1, j))
    if j > 0 and matrix[i][j - 1] in ("-", "L", "F"):
        pipe_boundaries.append(i * n + j - 1 if unidim else Coord(i, j - 1))
    if j < n - 1 and matrix[i][j + 1] in ("-", "J", "7"):
        pipe_boundaries.append(i * n + j + 1 if unidim else Coord(i, j + 1))

    return pipe_boundaries


def get_adjacent_ground(matrix: List[Tuple[str]], i: int, j: int) -> List[Coord]:
    """Returns the coordinates of the adjacent ground ('.') to the given coordinates (i, j)"""
    adj_grounds = list()

    if matrix[i - 1][j - 1] == ".":
        adj_grounds.append(Coord(i - 1, j - 1))
    if matrix[i - 1][j] == ".":
        adj_grounds.append(Coord(i - 1, j))
    if matrix[i - 1][j + 1] == ".":
        adj_grounds.append(Coord(i - 1, j + 1))
    if matrix[i][j + 1] == ".":
        adj_grounds.append(Coord(i, j + 1))
    if matrix[i + 1][j + 1] == ".":
        adj_grounds.append(Coord(i + 1, j + 1))
    if matrix[i + 1][j] == ".":
        adj_grounds.append(Coord(i + 1, j))
    if matrix[i + 1][j - 1] == ".":
        adj_grounds.append(Coord(i + 1, j - 1))
    if matrix[i][j - 1] == ".":
        adj_grounds.append(Coord(i, j - 1))

    return adj_grounds


def flood_fill(matrix: List[List[str]], start: Coord, fill_char: str) -> int:
    """Performs a flood fill algorithm starting from the given coordinates and fills all connected '.' with the given fill_char"""

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = [start]
    filled = 1
    matrix[start.X][start.Y] = fill_char

    while queue:
        current = queue.pop(0)

        for d in dirs:
            adj = Coord(current.X + d[0], current.Y + d[1])
            if matrix[adj.X][adj.Y] == ".":
                queue.append(adj)
                matrix[adj.X][adj.Y] = fill_char
                filled += 1

    return filled


def read_file() -> List[List[str]]:
    matrix = list()
    with open(abs_file_path) as f:
        for line in f:
            matrix.append(["#"] + [tile for tile in line.strip()] + ["#"])

    matrix.insert(0, ["#"] * len(matrix[0]))
    matrix.append(["#"] * len(matrix[0]))

    return matrix


part1()
part2()
