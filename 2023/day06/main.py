import os
import re
from typing import List, Tuple

from utils.timer import timer


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


"""
Since we can't count the ms spent holding the button,
the recordance travelled can be calculated as 
    d = remaining_time * button_held_time

This gives us a curve of recordance travelled
We just have to find when this curve starts
and ends being greater than the record

3 Solutions
 1. Iterate from beginning and end until find the limits
 2. Same as before, but with a binary search
 3. Find the roots of the curve described above
"""


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


part2()
