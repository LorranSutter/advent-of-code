import os
import math
from dataclasses import dataclass
from typing import List, Tuple, Set

import matplotlib.pyplot as plt

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Preprocessing:
- Since we have to connect the boxes based on the smallest distance, we first calculate the distances between all pairs of boxes
- We sort the distances in ascending order
- For both parts, we iterate through the sorted distances to connect the boxes
  1. If neither the boxes are in a existing circuit, we add them to a new circuit
  2. If both boxes are in the same circuit, we skip to the next distance
  3. If both boxes are in different circuits, we merge the circuits
  4. If only one box is in a circuit, we add the other box to that circuit

Part 1:
- After processing all distances, we sort the circuits by size and calculate the product of the sizes

Part 2:
- We keep iterating through the distances until all boxes are connected into a single circuit
- When the size of the only existing circuit equals the number of boxes, we know we reached the last two boxes connected 
"""


@dataclass(frozen=True)
class Distance:
    dist: float
    v1: Tuple[int]
    v2: Tuple[int]


@timer
def part1():
    boxes = parse_file()

    # Distance array
    d = calculate_distances(boxes)
    d.sort(key=lambda x: x.dist)

    circuits = []
    for i in range(len(boxes)):
        set_v1 = in_set(d[i].v1, circuits)
        set_v2 = in_set(d[i].v2, circuits)

        if set_v1 == -1 and set_v2 == -1:
            circuits.append({d[i].v1, d[i].v2})
        elif set_v1 == set_v2:
            continue
        elif set_v1 != -1 and set_v2 != -1:
            new_set = circuits[set_v1].union(circuits[set_v2])
            circuits.pop(max(set_v1, set_v2))
            circuits.pop(min(set_v1, set_v2))
            circuits.append(new_set)
        elif set_v1 != -1:
            circuits[set_v1].add(d[i].v2)
        elif set_v2 != -1:
            circuits[set_v2].add(d[i].v1)

    circuits.sort(key=lambda x: len(x))

    prod = 1
    for s in circuits[-3:]:
        prod *= len(s)

    print("Product of the first three largest circuits:", prod)

    # plot_boxes(boxes, circuits)


@timer
def part2():
    boxes = parse_file()

    # Distance array
    d = calculate_distances(boxes)
    d.sort(key=lambda x: x.dist)

    circuits = []
    last_boxes = tuple()
    for i in range(len(d)):
        set_v1 = in_set(d[i].v1, circuits)
        set_v2 = in_set(d[i].v2, circuits)

        if set_v1 == -1 and set_v2 == -1:
            circuits.append({d[i].v1, d[i].v2})
        elif set_v1 == set_v2:
            continue
        elif set_v1 != -1 and set_v2 != -1:
            new_set = circuits[set_v1].union(circuits[set_v2])
            circuits.pop(max(set_v1, set_v2))
            circuits.pop(min(set_v1, set_v2))
            circuits.append(new_set)
        elif set_v1 != -1:
            circuits[set_v1].add(d[i].v2)
        elif set_v2 != -1:
            circuits[set_v2].add(d[i].v1)

        if len(circuits) == 1:
            if len(circuits[0]) == len(boxes):
                last_boxes = (d[i].v1, d[i].v2)
                break

    print(
        "Product of X coordinates of the last boxes connected:",
        last_boxes[0][0] * last_boxes[1][0],
    )

    # plot_boxes(boxes, circuits)


def calculate_distances(boxes: List[Tuple[int]]) -> int:
    """
    Calculates the distances between all pairs of boxes."""
    d = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            d.append(Distance(dist3(boxes[i], boxes[j]), boxes[i], boxes[j]))
    return d


def plot_boxes(boxes: List[Tuple[int]], sets: List[Set[Distance]]):
    """
    Plots the boxes and their connections in a 3D space.
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection="3d")

    x_vals = [b[0] for b in boxes]
    y_vals = [b[1] for b in boxes]
    z_vals = [b[2] for b in boxes]

    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.set_zlabel("Z-Axis")

    ax.scatter(x_vals, y_vals, z_vals)

    # Point labels
    for i in range(len(boxes)):
        ax.text(
            x_vals[i],
            y_vals[i],
            z_vals[i],
            f"{x_vals[i], y_vals[i], z_vals[i]}",
        )

    # Connecting points
    for s in sets:
        for i in range(len(s) - 1):
            for j in range(i + 1, len(s)):
                v1 = list(s)[i]
                v2 = list(s)[j]
                ax.plot(
                    [v1[0], v2[0]],
                    [v1[1], v2[1]],
                    [v1[2], v2[2]],
                    color="green",
                    alpha=0.5,
                )

    plt.show()


def in_set(box: Tuple[int], sets: List[Set[Distance]]) -> bool:
    """
    Returns the index of the set containing the box, or -1 if not found
    """
    for i, s in enumerate(sets):
        if box in s:
            return i
    return -1


def dist3(v1: Tuple[int], v2: Tuple[int]):
    a, b, c = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
    return math.sqrt(a * a + b * b + c * c)


def parse_file() -> List[Tuple[int]]:
    boxes = []
    with open(abs_file_path) as f:
        for line in f:
            boxes.append(tuple(map(int, line.strip().split(","))))

    return boxes


part2()
