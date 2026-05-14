import os
from typing import Tuple
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- We just read the input file and parse it into a list of strings (steps)

Part 1:
- Straightforward implementation of the hash function described in the puzzle
- We calculate the hash for each step and sum up all the results

Part 2:
- Here is pretty much an implementation of a hash table with buckets (slots)
- We define a fixed size array of size 256 that will store the labels of the boxes
- Each index of the array is the hash result of the hash function that points to a list of lenses (slots)
- We just have to perform the operations to add or removing lenses for each step
- Finally, we sum up all the focal lengths according to the puzzle description
"""


@dataclass
class Len:
    label: str
    focal_length: int


@timer
def part1():
    sequence = parse_file("input.txt")

    total = sum((hash_step(step) for step in sequence))

    print(f"Total after {len(sequence)} steps: {total}")


@timer
def part2():
    sequence = parse_file("input.txt")

    boxes = tuple([] for _ in range(256))

    for step in sequence:
        if step[-1] == "-":
            label = step[:-1]
            h = hash_step(label)

            if boxes[h] != []:
                for l in boxes[h]:
                    if l.label == label:
                        boxes[h].remove(l)
                        break

        else:
            label, length = step.split("=")
            h = hash_step(label)

            if boxes[h] == []:
                boxes[h].append(Len(label, int(length)))
            else:
                found_len = False
                for l in boxes[h]:
                    if l.label == label:
                        l.focal_length = int(length)
                        found_len = True
                        break

                if not found_len:
                    boxes[h].append(Len(label, int(length)))

    focusing_power = 0
    for box_id, box in enumerate(boxes):
        for i, l in enumerate(box, 1):
            focusing_power += (box_id + 1) * i * l.focal_length

    print(f"Focusing power: {focusing_power}")


def hash_step(step: str) -> int:
    result = 0
    for c in step:
        result = ((result + ord(c)) * 17) % 256

    return result


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    sequence = []
    with open(abs_file_path, "r") as f:
        sequence = f.read().strip().split(",")
    return sequence


part1()
part2()
