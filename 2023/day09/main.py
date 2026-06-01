import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse each line into a list of integers

Part 1:
- For each history, generate sequences of differences between consecutive values
- Continue generating difference sequences until all values in a sequence are equal
  (we don't need to reach all zeros, just all equal values)
- During each iteration, store the last value of the sequence
- Once we reach a sequence with all equal values, sum all the stored last values
- This sum represents the next extrapolated value for that history
- Sum all extrapolated values across all histories

    Example visualization:
        0   3   6   9  12  15  [18]  <- Sum of last values: 15 + 3 + 0 = 18
          3   3   3   3   3   [3]
            0   0   0   0   [0]

Part 2:
- Similar to Part 1, but we extrapolate backwards instead of forwards
- For each history, generate the same sequences of differences
- During each iteration, store the first value of the sequence instead of the last
- Once we reach a sequence with all equal values, work backwards through the stored first values
- Calculate the previous value by subtracting: new_value = first_value - new_value
- This gives us the extrapolated value to the left of the original history
- Sum all extrapolated values across all histories

    Example visualization:
        [5]  10  13  16  21  30  45  <- Working backwards: 10 - (3 - (-2 - (2 - 0))) = 5
          [5]   3   3   5   9  15
            [-2]  0   2   4   6
              [2]  2   2   2
                [0]  0   0
"""


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    histories = parse_file()

    total_new_values = 0
    for values in histories:
        last_values = [values[-1]]
        while True:
            prediction = [0 for _ in range(len(values) - 1)]
            for i in range(len(values) - 1):
                prediction[i] = values[i + 1] - values[i]
            last_values.append(prediction[-1])

            if all_equal(prediction):
                break

            values = prediction.copy()

        total_new_values += sum(last_values)

    print("Sum extrapolated values:", total_new_values)


@timer
def part2():
    histories = parse_file()

    total_new_values = 0
    for values in histories:
        first_values = [values[0]]
        while True:
            prediction = [0 for _ in range(len(values) - 1)]
            for i in range(len(values) - 1):
                prediction[i] = values[i + 1] - values[i]
            first_values.append(prediction[0])

            if all_equal(prediction):
                break

            values = prediction.copy()

        new_value = 0
        for i in range(len(first_values) - 1, -1, -1):
            new_value = first_values[i] - new_value

        total_new_values += new_value

    print("Sum extrapolated values:", total_new_values)


def all_equal(l: List[int]) -> bool:
    current_value = l[0]
    for i in range(1, len(l)):
        if current_value != l[i]:
            return False
        current_value = l[i]
    return True


def parse_file() -> List[List[int]]:
    histories = list()
    with open(abs_file_path) as f:
        for line in f:
            histories.append(list(map(int, line.strip().split())))

    return histories


part1()
part2()
