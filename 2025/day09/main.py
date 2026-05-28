import os
from shapely import Polygon, box, plotting as pl
from typing import List, Tuple

import matplotlib.pyplot as plt

from utils.timer import timer
from utils.utils import tcolors

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Preprocessing:
- Read the input file and return a list of points

Part 1:
- This is a brute force approach, where we just calculat all possible rectangle areas and find the largest one

Part 2:
- Here we execute a similar brute force approach to Part 1, testing all possible pairs of points as rectangle corners
- However, Part 2 has a tricky polygon shape where the largest rectangle formed by any two points might extend outside the polygon boundaries
- Simply calculating the maximum area by point pairs isn't sufficient - we must verify that each candidate rectangle is completely contained within the polygon
- For every pair of points, we:
  1. Construct a rectangle using them as opposite corners
  2. Check if this rectangle is fully inside the polygon using Shapely's "contains" function
  3. Only if contained, compare its area against the current maximum
- This ensures we find the largest valid rectangle that fits entirely within the polygon's boundaries
"""


@timer
def part1():
    points = parse_file()

    max_area = 0
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            # +1 because both points are inclusive
            area = abs(
                (points[i][0] - points[j][0] + 1) * (points[i][1] - points[j][1] + 1)
            )
            if area > max_area:
                max_area = area

    print("Largest area:", max_area)


@timer
def part2():
    points = parse_file()
    polygon = Polygon(points)

    max_area = 0
    max_rect = None
    for i in range(len(points)):
        p0 = points[i]
        for j in range(len(points)):
            p1 = points[j]

            # Skip rectangles with no area
            if p0[0] == p1[0] or p0[1] == p1[1]:
                continue

            p2 = (p0[0], p1[1])
            p3 = (p1[0], p0[1])

            rect_points = box(p0[0], p0[1], p1[0], p1[1])

            if polygon.contains(rect_points):
                area = (abs(p1[0] - p0[0]) + 1) * (abs(p1[1] - p0[1]) + 1)

                if area > max_area:
                    max_area = area
                    max_rect = rect_points
                    print(
                        f"Largest rect:  {tcolors.GREEN}{p0}, {p1}, {p2}, {p3}{tcolors.RESET} Area: {tcolors.YELLOW}{area}{tcolors.RESET}"
                    )

    print("Largest area of a rectangle inside the polygon:", max_area)
    pl.plot_polygon(polygon)
    pl.plot_polygon(max_rect, color="green")
    plt.show()


def parse_file() -> List[Tuple[int]]:
    points = []
    with open(abs_file_path) as f:
        for line in f:
            points.append(tuple(map(int, line.strip().split(","))))

    return points


part1()
part2()
