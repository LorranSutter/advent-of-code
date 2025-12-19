import os
import itertools

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    op_combinations = {}
    s = 0
    with open(abs_file_path) as f:
        for row in f:
            calibration, test_values = row.rstrip("\n").split(":")
            calibration = int(calibration)
            test_values = list(map(int, test_values.split()))

            s += evaluate(calibration, test_values, op_combinations, ("+", "*"))

    print("Total calibration result:", s)


@timer
def part2():
    op_combinations = {}
    s = 0
    with open(abs_file_path) as f:
        for row in f:
            calibration, test_values = row.rstrip("\n").split(":")
            calibration = int(calibration)
            test_values = list(map(int, test_values.split()))

            s += evaluate(calibration, test_values, op_combinations, ("+", "*", "||"))

    print("Total calibration result:", s)


def evaluate(calibration, test_values, op_combinations, ops):
    ops_size = len(test_values) - 1

    for op in getOpCombinations(op_combinations, ops, ops_size):
        partial = test_values[0]
        for i in range(ops_size):
            partial = execute(partial, test_values[i + 1], op[i])
            if partial >= calibration:
                break
        if partial == calibration:
            return partial

    return 0


def getOpCombinations(op_combinations, ops, size):
    if size in op_combinations:
        return op_combinations[size]
    op_combinations[size] = list(itertools.product(ops, repeat=size))
    return op_combinations[size]


def execute(a, b, op):
    if op == "+":
        return a + b
    if op == "*":
        return a * b
    return int(str(a) + str(b))


part2()
