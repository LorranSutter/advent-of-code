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
    width, height = len(platform), len(platform[0])

    total_load = 0
    for j in range(width):
        load = height
        for i in range(height):
            if platform[i][j] == "O":
                total_load += load
                load -= 1
            elif platform[i][j] == "#":
                load = height - i - 1
    
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
