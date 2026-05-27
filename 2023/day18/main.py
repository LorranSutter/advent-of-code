import os
from typing import List, Tuple
from enum import Enum
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a list of Dig objects

Part 1:
- At first glence, we can clearly see the the borders of the trench forms an irregular polygon
- Intituitively, we just need to calculate the are of this polygon.
- The Shoelace formula is a well-known approach for this type of problem
    - However, this formula only calculates the area within the polygon
    - We also have to consider the border of the trench
- To solve that we do the following:
    - We iterate over the dig plan to calculate the corners of the polygon
    - In each iteration, we can update the partial area of the polygon witht the Shoelace formula
      along with the amount of meters of this specific edge
    - At the end, we just take the absolute value of the partial area, divide it by 2,
      and add 1 to get the total area, because walking on the border does not count the initial point

Part 2:
- First, we need to convert the color codes to instructions
- Then, the same approach from part 1 can be applied
"""


class Direction(Enum):
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    UP = "U"


@dataclass
class Dig:
    direction: Direction
    meters: int
    color: str


@timer
def part1():
    dig_plan = parse_file("input.txt")

    area = adapted_shoelace_formula(dig_plan)

    print(f"Cubic meters of lava in the trench: {area}")


@timer
def part2():
    dig_plan = parse_file("input.txt")
    dig_plan = [color_to_instruction(dig.color) for dig in dig_plan]

    area = adapted_shoelace_formula(dig_plan)

    print(f"Cubic meters of lava in the trench: {area}")


def adapted_shoelace_formula(dig_plan: List[Dig]) -> int:
    """Adapted Shoelace formula to calculate the area of the trench"""

    p0, p1 = (0, 0), (0, 0)
    area = 0
    for dig in dig_plan:
        match dig.direction:
            case Direction.UP:
                p1 = (p0[0], p0[1] - dig.meters)
            case Direction.DOWN:
                p1 = (p0[0], p0[1] + dig.meters)
            case Direction.LEFT:
                p1 = (p0[0] - dig.meters, p0[1])
            case Direction.RIGHT:
                p1 = (p0[0] + dig.meters, p0[1])

        # Normal steps of the Shoelace formula
        area += p0[0] * p1[1]
        area -= p0[1] * p1[0]

        # We add the borders of the trench to the partial area
        area += dig.meters

        p0 = p1

    # We add 1 at the end to also consider the initial point
    return abs(area) // 2 + 1


def color_to_instruction(color: str) -> Dig:
    meters = int(color[1:-1], 16)

    match color[-1]:
        case "0":
            return Dig(Direction.RIGHT, meters, color)
        case "1":
            return Dig(Direction.DOWN, meters, color)
        case "2":
            return Dig(Direction.LEFT, meters, color)
        case "3":
            return Dig(Direction.UP, meters, color)


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    dig_plan = []
    with open(abs_file_path, "r") as f:
        for line in f:
            direction, meters, color = line.strip().split(" ")
            color = color[1:-1]
            match direction:
                case "U":
                    dig_plan.append(Dig(Direction.UP, int(meters), color))
                case "D":
                    dig_plan.append(Dig(Direction.DOWN, int(meters), color))
                case "L":
                    dig_plan.append(Dig(Direction.LEFT, int(meters), color))
                case "R":
                    dig_plan.append(Dig(Direction.RIGHT, int(meters), color))
    return dig_plan


part1()
part2()
