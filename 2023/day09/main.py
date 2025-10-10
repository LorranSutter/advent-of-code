import os
from typing import List


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
No big deal here, maybe there is a more efficient way I don't see
For each history, just take de difference of sequencial pairs
Repeat untill all result values are equal (Don't have to reach the 0 row)
For each iteration store the last value for part 1 and first value for part 2

Iterate over the stored values
Part 1
    Sum all last values
Part 2
    Sum the diff between last value and current value
"""


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
