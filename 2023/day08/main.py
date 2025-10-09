import os
import re
import math
from itertools import cycle
from typing import Dict, Tuple
from dataclasses import dataclass


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


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    """
    Read instructions as string
    Create a dictionary of Nodes
        'AAA' -> Node(L='BBB', R='CCC')

    Iterate over instructions in a circular manner
    Starts with node AAA
    Go to the next node acoording to the instruction until finding ZZZ
    """
    instructions, nodes = parse_file()

    steps = 0
    current_node = 'AAA'
    for instruction in cycle(instructions):
        if current_node == 'ZZZ':
            break
        steps += 1
        current_node = nodes[current_node][instruction]

    print("Total steps:", steps)

def part2():
    """
    Read instructions as string
    Create a dictionary of Nodes
        'AAA' -> Node(L='BBB', R='CCC')

    Find all nodes that ends with A (starting nodes)
    Iterate over each starting node
    For each starting iterate over instructions in a circular manner
    Count how many steps each starting node takes to reach a Z node

    Since we should walk the nodes simultaneously, the ones that
    already reached a Z node will start walking the same path.

    If we want to find the total steps that all nodes need
    to get to a Z node at the same time, we just have to
    calculate the least common multiple of the total steps
    of each starting node
    """
    instructions, nodes = parse_file()
    starts = [node for node in nodes.keys() if node[-1] == 'A']

    steps_to_z = [0 for _ in range(len(starts))] 

    for i, current_node in enumerate(starts):
        for instruction in cycle(instructions):
            if current_node[-1] == 'Z':
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


part2()
