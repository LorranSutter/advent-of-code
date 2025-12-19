import os
from typing import List, Tuple
from dataclasses import dataclass

from utils.timer import timer


@dataclass
class Pipe:
    Left: int
    Right: int


@dataclass
class Coord:
    X: int
    Y: int


@dataclass
class Pipe2d:
    Left: Coord
    Right: Coord
    Outer: List[Coord]


script_dir = os.path.dirname(__file__)
rel_path = "input_sample.txt"
abs_file_path = os.path.join(script_dir, rel_path)

@timer
def part1():
    """
    Reads the whole matrix
    Parse the matrix to unidimensional array of adjacent pipes

    Get 2 pointers that leaves the starting point S and walk
    in oposite directions simultaneously. Count each iteration.
    The farthest point is when they find each other.
    """
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
    """
    Reads the whole matrix
    Parse the matrix to unidimensional array of adjacent pipes
    """
    matrix = read_file()
    start, pipes_matrix = parse_matrix_to_pipes_2(matrix)

    print(start)
    print(pipes_matrix)

    for row in pipes_matrix:
        for col in row:
            print(col)

    pipes_path = find_pipes_path(start, pipes_matrix)

    print(pipes_path)

    print(is_clockwise(pipes_path[0], pipes_path[1], pipes_path[2]))

    # TODO Try to check the orientation of the polygon
    # formed by the pipes https://github.com/LorranSutter/CVFEM/blob/master/geometry.py#L133
    # Use that to know what points are inside and outised of the pipes loop
    # For each point inside, make a graph trasversal to find all non adjacent points
    # Mark visited points and sum the results to know the total points inside the loop


def read_file() -> List[Tuple[str]]:
    matrix = list()
    with open(abs_file_path) as f:
        for line in f:
            matrix.append(tuple(tile for tile in line.strip()))

    return matrix


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
                        Pipe(*get_start_pipe_boundaries(matrix, i, j)),
                    )
                case _:
                    # We have to append non-pipes to make the unidimensional matrix work
                    pipe = Pipe(-1, -1)
            pipes.append(pipe)

    return start, pipes


def parse_matrix_to_pipes_2(
    matrix: List[Tuple[str]],
) -> Tuple[Tuple[Coord, Pipe2d], List[List[Pipe2d]]]:
    """
    Converts the 2-dim to a unidimensional array
    Each array element is a Pipe2d(left, right, outers), where
    left and right points to the array index of the adjacent pipe
    and outers are a list of adjacent ground ('.')
    """
    m, n = len(matrix), len(matrix[0])

    start = Tuple[Coord, Pipe2d]
    pipes_matrix = list(list())

    for i in range(m):
        row = list()
        for j in range(n):
            adj_grounds = get_adjacent_ground(matrix, i, j)
            match matrix[i][j]:
                case "|":
                    pipe = Pipe2d(Coord(i - 1, j), Coord(i + 1, j), adj_grounds)
                case "-":
                    pipe = Pipe2d(Coord(i, j - 1), Coord(i, j + 1), adj_grounds)
                case "L":
                    pipe = Pipe2d(Coord(i - 1, j), Coord(i, j + 1), adj_grounds)
                case "J":
                    pipe = Pipe2d(Coord(i - 1, j), Coord(i, j - 1), adj_grounds)
                case "7":
                    pipe = Pipe2d(Coord(i, j - 1), Coord(i + 1, j), adj_grounds)
                case "F":
                    pipe = Pipe2d(Coord(i, j + 1), Coord(i + 1, j), adj_grounds)
                case "S":
                    start = tuple(
                        [
                            Coord(i, j),
                            Pipe2d(
                                *get_start_pipe_boundaries(matrix, i, j, True),
                                adj_grounds,
                            ),
                        ]
                    )
                case _:
                    # We have to append non-pipes to make the unidimensional matrix work
                    pipe = Pipe2d(Coord(-1, -1), Coord(-1, -1), [])
            row.append(pipe)
        pipes_matrix.append(row)

    return start, pipes_matrix


def get_start_pipe_boundaries(
    matrix: List[Tuple[str]], i: int, j: int, pipe2d: bool = False
) -> List[Coord | int]:
    m, n = len(matrix), len(matrix[0])
    pipe_boundaries = list()

    # Only consider pipes that connects to S
    # In the following case, F is not connected
    # . | .
    # . S F
    # . J .
    if i > 0 and matrix[i - 1][j] in ("|", "7", "F"):
        pipe_boundaries.append(Coord(i - 1, j) if pipe2d else (i - 1) * n + j)
    if i < m - 1 and matrix[i + 1][j] in ("|", "L", "J"):
        pipe_boundaries.append(Coord(i + 1, j) if pipe2d else (i + 1) * n + j)
    if j > 0 and matrix[i][j - 1] in ("-", "L", "F"):
        pipe_boundaries.append(Coord(i, j - 1) if pipe2d else i * n + j - 1)
    if j < n - 1 and matrix[i][j + 1] in ("-", "J", "7"):
        pipe_boundaries.append(Coord(i, j + 1) if pipe2d else i * n + j + 1)

    return pipe_boundaries


def get_adjacent_ground(matrix: List[Tuple[str]], i: int, j: int) -> List[Coord]:
    m, n = len(matrix), len(matrix[0])
    adj_grounds = list()

    if i > 0 and j > 0 and matrix[i - 1][j - 1] == ".":
        adj_grounds.append(Coord(i - 1, j - 1))
    if i > 0 and matrix[i - 1][j] == ".":
        adj_grounds.append(Coord(i - 1, j))
    if i > 0 and j < n - 1 and matrix[i - 1][j + 1] == ".":
        adj_grounds.append(Coord(i - 1, j + 1))
    if j < n - 1 and matrix[i][j + 1] == ".":
        adj_grounds.append(Coord(i, j + 1))
    if i < m - 1 and j < n - 1 and matrix[i + 1][j + 1] == ".":
        adj_grounds.append(Coord(i + 1, j + 1))
    if i < m - 1 and matrix[i + 1][j] == ".":
        adj_grounds.append(Coord(i + 1, j))
    if i < m - 1 and j > 0 and matrix[i + 1][j - 1] == ".":
        adj_grounds.append(Coord(i + 1, j - 1))
    if j > 0 and matrix[i][j - 1] == ".":
        adj_grounds.append(Coord(i, j - 1))

    return adj_grounds


def find_pipes_path(
    start: Tuple[Coord, Pipe2d], pipes_matrix: List[List[Pipe2d]]
) -> List[Coord]:
    previous, next_pipe = start[0], start[1].Left
    pipe_path = list()
    while True:
        pipe_path.append(previous)
        # Got back to the starting point
        if next_pipe == start[0]:
            break

        # Make sure to not return back to the same pipe
        if previous != pipes_matrix[next_pipe.X][next_pipe.Y].Left:
            previous = next_pipe
            next_pipe = pipes_matrix[next_pipe.X][next_pipe.Y].Left
        else:
            previous = next_pipe
            next_pipe = pipes_matrix[next_pipe.X][next_pipe.Y].Right

    return pipe_path


def cross(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    return v1[0] * v2[1] - v2[0] * v1[1]


def is_clockwise(A: Coord, B: Coord, C: Coord) -> bool:
    """
    Get the 3 first points
    Make 2 vectors
    Calculate the cross product between the vectors
    It is clockwise if
    """

    v1 = (B.X - A.X, B.Y - A.Y)
    v2 = (C.X - B.X, C.Y - B.Y)

    return cross(v1, v2) < 0


part2()
