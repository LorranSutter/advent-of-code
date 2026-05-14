import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a 2D list of characters.

Part 1:
- We can calculate the total load without changing the platform (tilt)
- Instead of iterating over row, then column, we can iterate over column, then row
- Since the rocks will roll twards the north, we just have to keep track of the last empty cell in each column
- Starting with the maximum load, if we find a rounded rock ("O"), we add the current load to the total load, and decrement the load by 1
- If we find cube-shaped rock ("#"), we reset the load by its current position on the column - 1

Part 2:
- The trick here is to realize that after certain number of cycles, the platform state will start to repeat
- So, we simulate the spin cycle until, save each new state in an array, so we can check if the new calculate state has been seen before
- Once we find it, we can calculate the size of the loop cycle
- Obviously, the total of cycles will not be a multiple of the number of cycles, so we need to find the remainder
- With the remainder number in hands, we just have to get the corresponding state from the states array and calculate the total load on the north support beams
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

    print(f"Total load on the north support beams: {total_load}")


@timer
def part2():
    platform = parse_file("input.txt")
    cycles = 1000000000
    height, width = len(platform), len(platform[0])

    states = []

    print("Initial platform state:")
    print_platform(platform)
    print()

    # Find where the loop cycle starts
    loop_cycle = 0
    for i in range(cycles):
        spin_cycle(platform, height, width)
        if platform in states:
            loop_cycle = i
            break
        states.append([row[:] for row in platform])

    start_loop_cycle_id = states.index(platform)
    loop_cycle_size = loop_cycle - start_loop_cycle_id
    remaining_cycles = (cycles - 1 - start_loop_cycle_id) % loop_cycle_size

    last_state = states[start_loop_cycle_id + remaining_cycles]

    print("Last platform state:")
    print_platform(last_state)
    print()

    print(f"Loop detected after {i} cycles")
    print(f"Starting loop cycle ID: {start_loop_cycle_id}")
    print(f"Loop cycle size: {loop_cycle_size}")
    print(f"Remaining cycles after loop: {remaining_cycles}")

    # Calculate total load for the last state
    total_load = 0
    for j in range(width):
        for i in range(height):
            if last_state[i][j] == "O":
                total_load += height - i

    print(f"\nTotal load on the north support beams: {total_load}")


def spin_cycle(platform: List[List[str]], height: int, width: int) -> None:
    """Perform a full spin cycle: North, West, South, East."""
    tilt(platform, "N", height, width)
    tilt(platform, "W", height, width)
    tilt(platform, "S", height, width)
    tilt(platform, "E", height, width)


def tilt(platform: List[List[str]], direction: str, height: int, width: int) -> None:
    """
    Tilt the platform in the specified direction.

    Args:
        platform: The platform grid
        direction: One of 'N', 'S', 'E', 'W'
        height: Height of the platform
        width: Width of the platform
    """
    match direction:
        case "N":
            for j in range(width):
                empty_spot = 0
                for i in range(height):
                    if platform[i][j] == "O":
                        if empty_spot != i:
                            platform[empty_spot][j] = "O"
                            platform[i][j] = "."
                        empty_spot += 1
                    elif platform[i][j] == "#":
                        empty_spot = i + 1
        case "S":
            for j in range(width):
                empty_spot = height - 1
                for i in range(height - 1, -1, -1):
                    if platform[i][j] == "O":
                        if empty_spot != i:
                            platform[empty_spot][j] = "O"
                            platform[i][j] = "."
                        empty_spot -= 1
                    elif platform[i][j] == "#":
                        empty_spot = i - 1
        case "W":
            for i in range(height):
                empty_spot = 0
                for j in range(width):
                    if platform[i][j] == "O":
                        if empty_spot != j:
                            platform[i][empty_spot] = "O"
                            platform[i][j] = "."
                        empty_spot += 1
                    elif platform[i][j] == "#":
                        empty_spot = j + 1
        case "E":
            for i in range(height):
                empty_spot = width - 1
                for j in range(width - 1, -1, -1):
                    if platform[i][j] == "O":
                        if empty_spot != j:
                            platform[i][empty_spot] = "O"
                            platform[i][j] = "."
                        empty_spot -= 1
                    elif platform[i][j] == "#":
                        empty_spot = j - 1


def print_platform(platform: List[List[str]]):
    for line in platform:
        print("".join(line))


def parse_file(file_name: str) -> List[List[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    platform = []
    with open(abs_file_path, "r") as f:
        for line in f:
            platform.append([item for item in line.strip()])
    return platform


part1()
part2()