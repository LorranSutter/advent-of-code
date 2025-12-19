import os
from typing import List, Tuple

from utils.timer import timer


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Part 1:
- Two pointers strategy
- Starts pointing to the first two digits and always increment the second pointer
- If the value of the second is bigger than the first, the first points to the value of the second

Part 2:
- Pretty much a monotonic decreasing stack, but just implemented as an array
- Since the initial digits are always greater of equal to the next ones, we guarantee we will have the maximal possible joltage
- We iterate over the battery digits and check if this digit is greater than the last one incuded in the stack
- If so, we replace this last one by the new digit
    - The trick here is to keep checking previous digits while we don't find a smaller digit
    - Also, we have to account for the amount of remaining digits in the battery, because we need a total of 12 digits

Example:
    Stack: [9, 4, 3, 0, 0, 0]
    New digit: 5
    First iteration: [9, 4, 5, 0, 0, 0]
    Second iteration: [9, 5, 0, 0, 0, 0]
"""


@timer
def part1():
    batteries = parse_file()

    total_joltage = 0
    max_joltage = 0
    for battery in batteries:
        p0, p1 = 0, 1
        max_joltage = battery[p0] * 10 + battery[p1]
        while p0 < len(battery) - 1 and p1 < len(battery):
            max_joltage = max(max_joltage, battery[p0] * 10 + battery[p1])
            if battery[p0] < battery[p1]:
                p0 = p1
            p1 += 1

        total_joltage += max_joltage

    print("Total output joltage:", total_joltage)


@timer
def part2():
    batteries = parse_file()
    num_digits = 12

    total_joltage = 0
    for battery in batteries:
        max_joltages = [0 for _ in range(num_digits)]
        current_joltage_id = 0
        battery_length = len(battery)

        # Iterate over all digits in the battery
        for i, digit in enumerate(battery):
            current_joltage_id = pop_smaller_digits(
                max_joltages, digit, current_joltage_id, num_digits, battery_length - i
            )
            if current_joltage_id < num_digits - 1:
                current_joltage_id += 1

        # Calculate the total output joltage
        max_joltage_num = 0
        for joltage in max_joltages:
            max_joltage_num = max_joltage_num * 10 + joltage
        total_joltage += max_joltage_num

    print("Total output joltage:", total_joltage)


def pop_smaller_digits(
    max_joltages: List[int],
    digit: int,
    current_joltage_id: int,
    num_digits: int,
    remaining_battery_digits: int,
) -> int:
    """
    Remove smaller digits until we reach the first position
    Returns the index of the joltage that can be replaced
    """
    for i in range(current_joltage_id, -1, -1):
        # Prevents replacing more digits than available remaining battery digits
        if num_digits - i > remaining_battery_digits:
            break
        # Stops if we find a greater digit
        if digit <= max_joltages[i]:
            break
        # Guarantees the next digit will always be smaller
        if len(max_joltages) - 1 > i:
            max_joltages[i + 1] = 0

        max_joltages[i] = digit
        current_joltage_id = i

    return current_joltage_id


def parse_file() -> List[Tuple[int]]:
    batteries = []
    with open(abs_file_path) as f:
        for line in f:
            line = line.strip()
            line = tuple(int(battery) for battery in line)
            batteries.append(line)

    return batteries


part2()
