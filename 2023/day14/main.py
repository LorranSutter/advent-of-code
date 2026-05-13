import os
from typing import Tuple

from utils.timer import timer

"""
Preprocessing:
-

Part 1:
-

Part 2:
-
"""


@timer
def part1():
    platform = parse_file("input.txt")

    total_load = 0
    for j in range(len(platform[0])):
        max_load = len(platform[0])
        for i in range(len(platform)):
            if platform[i][j] == "O":
                total_load += max_load
                max_load -= 1
            elif platform[i][j] == "#":
                max_load = len(platform[0]) - i - 1
    
    print(f"Total load: {total_load}")


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample.txt")
    pass


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    platform = []
    with open(abs_file_path, "r") as f:
        for line in f:
            platform.append([item for item in line.strip()])
    return platform


part1()
# part2()
