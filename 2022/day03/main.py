import os
from typing import Tuple

from utils.timer import timer

"""
Part 1:
- Each rucksack is one string; the first half is one compartment, the second half the other. The item packed
  wrong is the single type that shows up in both compartments, so we split the string down the middle and take
  the set intersection of the two halves — that leaves exactly one character. The (repeated,) unpacking is a
  cheap assertion that there really is exactly one.
- Turning that character into a priority is just an ord() shift, handled in two ranges:
    lowercase 'a'..'z' are ord 97..122 and need to map to 1..26  -> subtract 96
    uppercase 'A'..'Z' are ord 65..90  and need to map to 27..52 -> subtract 38 (since 65 - 38 = 27)
  So 'p' gives 112 - 96 = 16 and 'L' gives 76 - 38 = 38. We sum that priority over every rucksack.

Part 2:
- Same priority shift as part 1, but the shared item is the group badge now instead of the mispacked one. We
  walk the list three lines at a time and intersect all three rucksacks as sets — whole strings this time,
  not halves — which again leaves exactly one common character.
"""


@timer
def part1():
    rucksacks = parse_file("input.txt")

    total_priority = 0
    for rucksack in rucksacks:
        length = len(rucksack)
        first_half, second_half = rucksack[: length // 2], rucksack[length // 2 :]
        (repeated,) = set(first_half) & set(second_half)

        shift = 38 if repeated.isupper() else 96
        total_priority += ord(repeated) - shift

    print(f"Total priority: {total_priority}")


@timer
def part2():
    rucksacks = parse_file("input.txt")

    total_priority = 0
    for i in range(0, len(rucksacks), 3):
        (repeated,) = set(rucksacks[i]) & set(rucksacks[i + 1]) & set(rucksacks[i + 2])

        shift = 38 if repeated.isupper() else 96
        total_priority += ord(repeated) - shift

    print(f"Total priority: {total_priority}")


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    rucksacks = []
    with open(abs_file_path, "r") as f:
        for line in f:
            rucksacks.append(line.strip())
    return rucksacks


part1()
part2()
