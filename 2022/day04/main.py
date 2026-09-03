import os
import re
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Every line looks like "2-4,6-8", so one regex, (\\d+)-(\\d+),(\\d+)-(\\d+), grabs all four numbers in one go. We keep
  each pair as a flat 4-tuple (lo1, hi1, lo2, hi2) instead of two 2-tuples, and the part functions slice
  assignment[:2] and assignment[2:] to pull the two ranges back out.

Part 1:
- We count the pairs where one range fully swallows the other. Range a1 contains range a2 exactly when a1 starts no
  later and ends no earlier: a1[0] <= a2[0] and a1[1] >= a2[1]. We test that both ways round (a1 inside a2, or a2
  inside a1) and count the pair if either holds.

Part 2:
- Same loop as part 1, just "fully contains" swapped for "overlaps at all". The trick is we don't have to expand the
  ranges into sets of section IDs and compare them - two ranges overlap if and only if the later start point isn't
  past the earlier end point:

      max(a1[0], a2[0]) <= min(a1[1], a2[1])

  max(a1[0], a2[0]) is the start of whichever range starts later; min(a1[1], a2[1]) is the end of whichever range
  ends first. If that start sits at or before that end, the gap between them is a real, non-empty overlap.
"""


@timer
def part1():
    assignments = parse_file("input.txt")

    count = 0
    for assignment in assignments:
        if fully_contained(assignment[:2], assignment[2:]):
            count += 1

    print(f"Ranges that fully contain the other: {count}")


@timer
def part2():
    assignments = parse_file("input.txt")

    count = 0
    for assignment in assignments:
        if overlap(assignment[:2], assignment[2:]):
            count += 1

    print(f"Ranges that overlap: {count}")


def fully_contained(a1: Tuple[int, int], a2: Tuple[int, int]) -> bool:
    if a1[0] <= a2[0] and a1[1] >= a2[1]:
        return True

    if a2[0] <= a1[0] and a2[1] >= a1[1]:
        return True

    return False


def overlap(a1: Tuple[int, int], a2: Tuple[int, int]) -> bool:
    if max(a1[0], a2[0]) <= min(a1[1], a2[1]):
        return True

    return False


def parse_file(file_name: str) -> List[Tuple[int, int, int, int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    assignments = []
    with open(abs_file_path, "r") as f:
        for line in f:
            matches = re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", line)
            assignments.append(tuple(map(int, matches[0])))
    return assignments


part1()
part2()
