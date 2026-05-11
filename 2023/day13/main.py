import os
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
-

Part 1:
-

Part 2:
-
"""


# 29428 too low
@timer
def part1():
    islands = parse_file("input.txt")

    total = 0
    for island in islands:
        row_hashes, col_hashes = hash_island(island)

        row_mirror_indexes = get_mirror_indexes(row_hashes)
        col_mirror_indexes = get_mirror_indexes(col_hashes)

        summary = sum([100 * (id + 1) for id in row_mirror_indexes])
        summary += sum([id + 1 for id in col_mirror_indexes])

        total += summary

    print(f"Total: {total}")


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample.txt")
    pass


def get_mirror_indexes(lines: List[int]) -> int:
    """
    Returns the indexes of the lines that are mirrored in the list of lines
    """

    # Search for lines next to each other that are the same
    mirror_indexes = []
    for i in range(len(lines) - 1):
        if lines[i] == lines[i + 1]:
            mirror_indexes.append(i)

    # No reflection found for this island
    if mirror_indexes == []:
        return []

    # Check for reflections that are mirrored in both directions
    for mirror_index in mirror_indexes[:]:
        p1, p2 = mirror_index, mirror_index + 1
        while p1 >= 0 and p2 < len(lines):
            if lines[p1] != lines[p2]:
                # Invalid reflection found
                mirror_indexes.remove(mirror_index)
                break
            p1 -= 1
            p2 += 1

    return mirror_indexes


def hash_island(island: str) -> Tuple[List[int], List[int]]:
    """
    Returns the hash of each row and column of the island for faster comparison
    """
    island = island.split("\n")

    cols = ["" for _ in range(len(island[0]))]
    for j in range(len(island[0])):
        for i in range(len(island)):
            cols[j] += island[i][j]

    row_hashes = [hash(row) for row in island]
    col_hashes = [hash(col) for col in cols]

    return row_hashes, col_hashes


def parse_file(file_name: str) -> List[Tuple[List[int], List[int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        return f.read().split("\n\n")


part1()
# part2()
