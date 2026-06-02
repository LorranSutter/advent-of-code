import os
import re
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Read the input file to parse the list of race durations and record distances
- Duration and record values are separated by spaces under 'Time:' and 'Distance:' lines

Part 1:
- For each race, determine how many ways the boat can beat the record distance
- Holding the button for ms milliseconds charges the boat speed to ms millimeters/millisecond, and the boat moves for the remaining (time - ms) milliseconds
- The distance travelled is: d = ms * (time - ms)
- Find the lower and upper bounds of holding times that exceed the record by scanning from the beginning and end respectively
- Multiply the number of winning ways ($end - start + 1$) for all races together and print the product

Part 2:
- Concatenate the individual numbers of the input (times and records) to form a single, much larger race
- Perform the same search for lower and upper bounds of winning holding times, calculate the total ways to beat the record, and print the result
"""


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    times, records = parse_file()
    times = tuple(map(int, times))
    records = tuple(map(int, records))

    total = 1
    for time, record in zip(times, records):
        start, end = find_curve_limits(time, record)
        total *= end - start + 1

    print("Number of ways to beat the record:", total)


@timer
def part2():
    times, records = parse_file()
    time = int("".join(times))
    record = int("".join(records))

    start, end = find_curve_limits(time, record)

    print("Number of ways to beat the record:", end - start + 1)


def find_curve_limits(time: int, record: int):
    start, end = 0, 0
    for ms in range(1, time):
        if (time - ms) * ms > record:
            start = ms
            break

    for ms in range(time, 0, -1):
        if (time - ms) * ms > record:
            end = ms
            break

    return start, end


def parse_file() -> Tuple[List[str], List[str]]:
    times, records = list(), list()
    with open(abs_file_path) as f:
        times = f.readline().split(":")[1]
        times = re.split(r"\s+", times.strip())

        records = f.readline().split(":")[1]
        records = re.split(r"\s+", records.strip())

    return times, records


part1()
part2()
