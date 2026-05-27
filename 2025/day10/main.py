import os
from dataclasses import dataclass
from typing import List, Tuple
from itertools import combinations_with_replacement

@dataclass
class Schematics:
    size: int
    indicator: int
    buttons: List[int]
    joltages: List[int]


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Explanation
"""


def part1():
    schematics = parse_file()

    num_toggles = []
    for schematic in schematics:
        # print(schematic)
        for i in range(1, len(schematic.buttons)+1):
            combo_size = try_toggle(schematic, i)
            if combo_size > 0:
                num_toggles.append(combo_size)
                break
    
    print(num_toggles)
    print(sum(num_toggles))

def try_toggle(schematic, size):
    for combo in combinations_with_replacement(schematic.buttons, size):
        toggle = 0
        for combo_button in combo:
            toggle ^= combo_button
        if toggle == schematic.indicator:
            print(schematic, combo)
            return len(combo)
    return 0

def part2():
    # TODO: Implement part 2
    # This is a Linear Algebra problem. Just have to create the right model and implement it
    pass


def parse_file() -> List[Tuple[int]]:
    schematics = []
    with open(abs_file_path) as f:
        for line in f:
            line = line.strip().split()

            # Remove brackets and convert indicator to binary
            indicator = line[0][1:-1][::-1]
            size = len(indicator)
            indicator = indicator.replace(".", "0").replace("#", "1")
            indicator = int(indicator, 2)

            # Remove parenthesis and convert buttons to integers
            buttons = []
            for button in line[1:-1]:
                button = list(map(int,button[1:-1].split(',')))
                binary = 0
                for digit in button:
                    binary |= 1 << digit
                buttons.append(binary)

            # Remove curly braces and convert joltages to integers
            joltages = list(map(int, line[-1][1:-1].split(",")))

            schematics.append(Schematics(size, indicator, buttons, joltages))

    return schematics


part1()
