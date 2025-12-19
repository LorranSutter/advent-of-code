import os

from utils.timer import timer


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
The idea here is just interpreting R as positive rotation and L as negative rotation.
We add the rotation to the current dial and keep it within the range of 0-99, doing modulo 100

Part 1:
    - Just count the number of times the dial ends pointing to 0
Part 2:
    - We do the same as part 1
    - Plus, count the number of total rotations. For cases where the rotation is > 100
    - After total rotation, if there is a remainder, we check if that with current dial
      would cause the dial to cross the 0 mark
"""


@timer
def part1():
    rotations = parse_file()

    dial, count = 50, 0
    for rotation in rotations:
        dial = (dial + rotation) % 100
        if dial == 0:
            count += 1

    print("Password:", count)


@timer
def part2():
    rotations = parse_file()

    dial, count = 50, 0
    for rotation in rotations:
        # Check when dial ends pointing to 0
        dial = (dial + rotation) % 100
        if dial == 0:
            count += 1

        # Count complete rotations
        count += abs(rotation) // 100

        # Check if the remaining rotation would cause the dial to cross the 0 mark
        if rotation > 0 and dial < (rotation % 100) and dial != 0:
            count += 1
        elif rotation < 0 and dial > 100 - (abs(rotation) % 100):
            count += 1

    print("Password:", count)


def parse_file():
    rotations = []
    with open(abs_file_path) as f:
        for line in f:
            rotation = line.rstrip("\n")
            if rotation[0] == "R":
                rotations.append(int(rotation[1:]))
            else:
                rotations.append(-int(rotation[1:]))

    return rotations


part2()
