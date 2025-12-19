import os
import re

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    s = 0
    with open(abs_file_path) as f:
        memory = f.read()
        pairs = re.findall("mul\((\d+),(\d+)\)", memory)

        for pair in pairs:
            s += int(pair[0]) * int(pair[1])

    print("Sum:", s)


@timer
def part2():
    s = 0
    with open(abs_file_path) as f:
        memory = f.read()
        words = re.findall("mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)

        enabled = True
        for word in words:
            if word == "do()":
                enabled = True
            elif word == "don't()":
                enabled = False
            elif enabled:
                s += multiply(word)

    print("Sum:", s)


def multiply(op):
    nums = re.findall("\d+", op)
    return int(nums[0]) * int(nums[1])


part2()
