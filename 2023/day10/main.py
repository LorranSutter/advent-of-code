import os
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Node:
    Left: int
    Right: int


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


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


def part2():
    pass


def read_file() -> List[Tuple[str]]:
    matrix = list()
    with open(abs_file_path) as f:
        for line in f:
            matrix.append(tuple(tile for tile in line.strip()))

    return matrix


def parse_matrix_to_pipes(matrix: List[Tuple[str]]) -> Tuple[Node, List[Node]]:
    """
    Converts the 2-dim to a unidimensional array
    Each array element is a Node(left, right), where
    left and right points to the array index of the adjacent pipe
    """
    m, n = len(matrix), len(matrix[0])

    start = Tuple[int, Node]
    pipes = list()

    for i in range(m):
        for j in range(n):
            match matrix[i][j]:
                case "|":
                    pipe = Node((i - 1) * n + j, (i + 1) * n + j)
                case "-":
                    pipe = Node(i * n + j - 1, i * n + j + 1)
                case "L":
                    pipe = Node((i - 1) * n + j, i * n + j + 1)
                case "J":
                    pipe = Node((i - 1) * n + j, i * n + j - 1)
                case "7":
                    pipe = Node(i * n + j - 1, (i + 1) * n + j)
                case "F":
                    pipe = Node(i * n + j + 1, (i + 1) * n + j)
                case "S":
                    start = (
                        i * n + j,
                        Node(*get_start_pipe_boundaries(matrix, i, j)),
                    )
                case _:
                    # We have to append non-pipes to make the unidimensional matrix work
                    pipe = Node(-1, -1)
            pipes.append(pipe)

    return start, pipes


def get_start_pipe_boundaries(matrix: List[Tuple[str]], i: int, j: int) -> List[int]:
    m, n = len(matrix), len(matrix[0])
    pipe_boundaries = list()

    # Only consider pipes that connects to S
    # In the following case, F is not connected
    # . | .
    # . S F
    # . J .
    if i > 0 and matrix[i - 1][j] in ("|", "7", "F"):
        pipe_boundaries.append((i - 1) * n + j)
    if i < m - 1 and matrix[i + 1][j] in ("|", "L", "J"):
        pipe_boundaries.append((i + 1) * n + j)
    if j > 0 and matrix[i][j - 1] in ("-", "L", "F"):
        pipe_boundaries.append(i * n + j - 1)
    if j < n - 1 and matrix[i][j + 1] in ("-", "J", "7"):
        pipe_boundaries.append(i * n + j + 1)

    return pipe_boundaries


part1()
