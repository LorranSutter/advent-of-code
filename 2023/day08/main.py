import os
import re
import math
from itertools import cycle
from typing import Dict, Tuple
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Read the first line as a string of L/R instructions
- Parse the remaining lines using regex to extract node definitions
- Build a dictionary mapping each node name to a Node dataclass containing its left and right neighbors
  Example: 'AAA' -> Node(L='BBB', R='CCC')

Part 1:
- Start at node 'AAA' and follow the instructions in a circular manner (using itertools.cycle)
- For each instruction ('L' or 'R'), move to the corresponding neighbor node
- Count the number of steps taken until reaching node 'ZZZ'
- The instructions repeat indefinitely if we haven't reached the destination yet

    Example:
        Instructions: RL
        AAA -> (R) -> CCC -> (L) -> ZZZ
        Total steps: 2

Part 2:
- Find all nodes ending with 'A' - these are our simultaneous starting positions
- For each starting node, independently count how many steps it takes to reach any node ending with 'Z'
- Store the step count for each starting node
- The key insight: each path from an 'A' node to a 'Z' node forms a cycle
- Since all paths must align to have all nodes end with 'Z' simultaneously, we need to find when all cycles sync up
- This synchronization point is the Least Common Multiple (LCM) of all individual step counts
- Calculate and return the LCM of all step counts

    Example:
        Starting nodes: 11A, 22A
        11A reaches 11Z in 2 steps
        22A reaches 22Z in 3 steps
        LCM(2, 3) = 6 steps (when both are at Z nodes simultaneously)
"""

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@dataclass
class Node:
    L: str
    R: str

    # To make the class subscriptable, node["L"]
    def __getitem__(self, key):
        if key == "L":
            return self.L
        elif key == "R":
            return self.R
        else:
            raise KeyError(f"Invalid key: {key}")


@timer
def part1():
    instructions, nodes = parse_file()

    steps = 0
    current_node = "AAA"
    for instruction in cycle(instructions):
        if current_node == "ZZZ":
            break
        steps += 1
        current_node = nodes[current_node][instruction]

    print("Total steps:", steps)


@timer
def part2():
    instructions, nodes = parse_file()
    starts = [node for node in nodes.keys() if node[-1] == "A"]

    steps_to_z = [0 for _ in range(len(starts))]

    for i, current_node in enumerate(starts):
        for instruction in cycle(instructions):
            if current_node[-1] == "Z":
                break
            steps_to_z[i] += 1
            current_node = nodes[current_node][instruction]

    print("Total steps:", math.lcm(*steps_to_z))


def parse_file() -> Tuple[str, Dict[str, Node]]:
    instructions = ""
    nodes = dict()
    with open(abs_file_path) as f:
        instructions = f.readline().strip()
        # Skip empty line
        f.readline()

        # Read the nodes
        for line in f:
            match = re.search(r"(\w{3})\s=\s\((\w{3}),\s(\w{3})\)", line)
            nodes[match.group(1)] = Node(match.group(2), match.group(3))

    return instructions, nodes


part1()
part2()
