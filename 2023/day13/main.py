import os
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Read the input file and split each island.
- The trick here is to preprocess the island input to facilitate comparison.
    - We separate each island into two lists of lists: one for the rowns and one for the columns.
    - For part 1, we can hash each row and column.
    - For part 2, we convert each row and column into binary representation, where # is 1 and . is 0.

Part 1:
- For each island, we first hash each row and column.
- Then, we can call the get_mirror_indexes function to find the mirror indexes for the set of rows and the set of columns.
- Having the indexes of the morrored rows and columns, we can calculate the summary.

Part 2:
- For each island, we first convert each row and column into binary representation.
- The binary conversion is a better approach, because it makes it easier to identify if two binaries have only one bit different:
    - a ^ b will return the difference of the numbers
    - If they have only one bit different, the result will be a power of 2
        281       -> 100011001
        265       -> 100001001
        281 ^ 265 -> 000010000 -> 16
    - To know if there is only one bit different, we can do the following trick:
        16 & (16 - 1) -> 10000 & 01111 -> 0
    - If the result is 0, then the binary representations have only one bit different.
- Here, we can't use the get_mirror_indexes function because it assumes there will be at least a pair of adjacent lines that are equal.
- So, the following case will be missed:
    #...##..#
    #....#..#
- Instead, we use the function is_smudge_fixable to check every pair of lines on the rowns and the columns.
- This function checks the binary diff described above for each pair in the rowns and columns.
- If there is only one smudge, then we add it to the summary.
- Also, since we will be fixing the smudge, any previous valid mirrorings will be invalidated. So we don't need to consider them.

Obs: Using binary conversion would also work for part 1, but I only had this idea for part 2, so I left it as is.
"""


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
    islands = parse_file("input.txt")

    total = 0
    for island in islands:
        rows, cols = to_binary(island)

        summary = 0
        for i in range(len(rows)):
            if is_smudge_fixable(rows, i):
                summary += 100 * (i + 1)

        for j in range(len(cols)):
            if is_smudge_fixable(cols, j):
                summary += j + 1

        total += summary

    print(f"Total: {total}")


def get_mirror_indexes(lines: List[int]) -> List[int]:
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


def is_smudge_fixable(lines: List[int], id: int) -> bool:
    smuges_fixed = 0
    p1, p2 = id, id + 1
    while p1 >= 0 and p2 < len(lines):
        if lines[p1] != lines[p2]:
            # Only 1 smudge can be fixed
            if smuges_fixed > 0:
                return False

            # There could be only one smudge per line
            diff = lines[p1] ^ lines[p2]
            # e.g. 256 & (256 - 1) == 0, but 257 & (257 - 1) > 0
            if diff & (diff - 1) > 0:
                return False

            smuges_fixed += 1
        p1 -= 1
        p2 += 1

    return smuges_fixed == 1


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


def to_binary(island: str) -> Tuple[List[bin], List[bin]]:
    """
    Converts the island to binary representation for faster comparison
    """
    island = island.split("\n")

    # # -> 1
    # . -> 0

    rows = []
    for i in range(len(island)):
        rows.append(0)
        for j in range(len(island[0])):
            rows[i] = rows[i] << 1
            if island[i][j] == "#":
                rows[i] |= 1

    cols = [0 for _ in range(len(island[0]))]
    for j in range(len(island[0])):
        for i in range(len(island)):
            cols[j] = cols[j] << 1
            if island[i][j] == "#":
                cols[j] |= 1

    return rows, cols


def parse_file(file_name: str) -> List[Tuple[List[int], List[int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        return f.read().split("\n\n")


part1()
part2()
