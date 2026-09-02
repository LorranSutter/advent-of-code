import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- The input lists each elf's food items one per line, with a blank line between elves. Splitting the whole file on
  "\n\n" gives one block of lines per elf, and we sum each block right away, so parse_file returns a flat list of
  per-elf calorie totals rather than the individual item values.
- That collapse is what makes both parts short: by the time parsing is done there are no items left to think about,
  just one number per elf.

Part 1:
- Once each elf is a single total, "which elf carries the most" is just the maximum of the list, so this is a
  straight max(items).

Part 2:
- Same idea as part 1, but instead of the single largest total we want the sum of the three largest. We sort the
  totals ascending and add up the last three with sum(sorted(items)[-3:]).
"""


@timer
def part1():
    items = parse_file("input.txt")

    max_calories = max(items)

    print(f"Max calories: {max_calories}")


@timer
def part2():
    items = parse_file("input.txt")

    sum_top_three = sum(sorted(items)[-3:])

    print(f"Sum top three: {sum_top_three}")


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    items = []
    with open(abs_file_path, "r") as f:
        data = f.read().split("\n\n")

    for d in data:
        items.append(sum(map(int, d.strip().split("\n"))))

    return items


part1()
part2()
