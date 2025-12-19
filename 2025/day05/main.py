import os
from typing import List, Tuple

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Part 1:
- Considering there are very few ranges, we can iterate over each ingredient ID and check if it falls within any range.

Part 2:
- Since we have overlapping ranges, we can merge them first to form non-overlapping intervals.
- Then, the number of ingredients will be the difference between the start and end of each merged interval summed up.

- We just have to be aware that when we merge two ranges, this new merged range might overlap with other ranges
  So we need to re-check from the start every time we merge a range.
"""


@timer
def part1():
    ranges, ids = parse_file()
    fresh_ingredients = 0

    for id in ids:
        for interval in ranges:
            if interval[0] <= id <= interval[1]:
                fresh_ingredients += 1
                break

    print("Number of fresh ingredients", fresh_ingredients)


@timer
def part2():
    ranges, _ = parse_file()
    fresh_ingredients = 0

    i, j = 0, 0
    while True:
        if i >= len(ranges):
            break

        j = 0
        while True:
            if j >= len(ranges):
                break
            if i == j:
                j += 1
                continue

            ok, new_range = merge_ranges(ranges[i], ranges[j])
            if ok:
                ranges[i] = new_range
                ranges.pop(j)
                i -= 1
                break
            j += 1
        i += 1

    # +1 because both ends are inclusive
    fresh_ingredients = sum([interval[1] - interval[0] + 1 for interval in ranges])

    print("Number of fresh ingredients", fresh_ingredients)


def merge_ranges(r1: List[Tuple], r2: List[Tuple]) -> Tuple[bool, List[Tuple]]:
    if max(r1[0], r2[0]) <= min(r1[1], r2[1]):
        return True, (min(r1[0], r2[0]), max(r1[1], r2[1]))
    return False, None


def parse_file() -> Tuple[List[Tuple], List[int]]:
    ranges, ids = [], []
    with open(abs_file_path) as f:
        for line in f:
            if line.strip() == "":
                break
            ranges.append(list(map(int, line.strip().split("-"))))

        for line in f:
            ids.append(int(line.strip()))

    return ranges, ids


part2()
