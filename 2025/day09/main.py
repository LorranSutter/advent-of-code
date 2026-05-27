import os
from enum import Enum
from shapely import Polygon, LineString, box, plotting as pl
from typing import List, Tuple, Set
from itertools import combinations

import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Explanation
"""


class TileType(Enum):
    EMPTY = 0
    TILE = 1


def part1():
    points = parse_file_1()

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


# 1566900820 too low, Rectangle: (93327, 48335) (3993, 65874) (93327, 65874) (3993, 48335) Area: 1566900820
# 1566935900
def part2():
    # TODO: Implement part 2
    # TODO: it is correct, just need formatting
    grid, points = parse_file_2()
    polygon = Polygon(points)
    print(polygon.area)
    # plot_grid(points, [], True)
    print(points)

    line = LineString([(4, 3), (8, 1)])
    print(polygon.contains(line))

    pl.plot_line(line, color="red")
    pl.plot_polygon(polygon)
    # plt.grid(False)

    # poly = Polygon([
    #             [0,4],
    #             [7,4],
    #             [7,2],
    #             [0,2]
    #             ])
    # pl.plot_polygon(poly, color="green")

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
                    print("Rectangle:", p0, p1, p2, p3, "Area:", area)

    print("Largest area of a rectangle:", max_area)
    pl.plot_polygon(max_rect, color="green")
    plt.show()


def plot_grid_map(grid: List[List[TileType]], label: bool = False):
    """
    Plots the boxes and their connections in a 3D space.
    """
    _, ax = plt.subplots()

    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid()
    ax.invert_yaxis()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == TileType.TILE:
                ax.scatter(i, j, color="red")

    # # Point labels
    # if labels:
    #     for i in range(len(points)):
    #         ax.text(
    #             x_vals[i],
    #             y_vals[i],
    #             f"{x_vals[i], y_vals[i]}",
    #         )

    # # Connecting points
    # for i in range(len(points) - 1):
    #     v1 = points[i]
    #     v2 = points[i + 1]
    #     ax.plot(
    #         [v1[0], v2[0]],
    #         [v1[1], v2[1]],
    #         color="green",
    #         alpha=0.5,
    #     )

    # if len(other_points) > 0:
    #     x_vals = [p[0] for p in other_points]
    #     y_vals = [p[1] for p in other_points]
    #     ax.scatter(x_vals, y_vals)

    plt.show()


# 4623297835 too high
def part2_old():
    points = parse_file_1()
    plot_grid(points, [], True)
    print(points)
    horizontal, vertical = get_edges(points)
    print("Horizontal edges:", horizontal)
    print("Vertical edges:", vertical)

    # max_area_points = []
    # max_area = 0
    # points_set = set(points)
    # inside = []
    # for i in range(len(points) - 1):
    #     for j in range(i + 1, len(points)):
    #         valid_rect = True
    #         # Other rectangle edges
    #         p1 = (points[i][0], points[j][1])
    #         p2 = (points[j][0], points[i][1])
    #         if p1 not in points_set and not in_polygon_2(p1, points):
    #             valid_rect = False
    #         if valid_rect and (p2 in points_set or in_polygon_2(p2, points)):
    #             inside.append(p1)
    #             inside.append(p2)
    #         else:
    #             valid_rect = False

    #         if valid_rect:
    #             area = abs(
    #                 (points[i][0] - points[j][0] + 1)
    #                 * (points[i][1] - points[j][1] + 1)
    #             )
    #             if area > max_area:
    #                 max_area = area
    #                 max_area_points = [p1, p2]

    # print(inside)
    # print("Largest area:", max_area)
    # plot_grid(points, max_area_points, False)


# Fix types
def get_edges(points: List[Tuple[int]]) -> Tuple[List[int], List[int]]:
    """
    Identifies the horizontal and vertical edges of the grid.
    """
    horizontal_edges = []
    vertical_edges = []
    p0 = points[0]

    # Append the first point to the end to close the loop
    for p in points[1:] + [p0]:
        if p0[0] == p[0]:
            vertical_edges.append(((p0[0], p0[1]), (p[0], p[1])))
        elif p0[1] == p[1]:
            horizontal_edges.append(((p0[0], p0[1]), (p[0], p[1])))
        p0 = p

    return horizontal_edges, vertical_edges


def check_intersection(seg1_points, seg2_points):
    x1, y1 = seg1_points[0]
    x2, y2 = seg1_points[1]
    x3, y3 = seg2_points[0]
    x4, y4 = seg2_points[1]

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return False  # Lines are parallel or collinear and do not have a unique intersection point.

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    # Check if the intersection point is within both line segments' bounds
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return True

    return False


def in_polygon_2(
    point: Tuple[int],
    horizontal_edges: List[Tuple[int]],
    vertical_edges: List[Tuple[int]],
) -> bool:
    is_inside = True
    for h in horizontal_edges:
        # TODO Fix params
        if check_intersection((h[0], h[1]), (point[0], point[1])):
            is_inside = False
            break
    if is_inside:
        for v in vertical_edges:
            # TODO Fix params
            if check_intersection((v[0], v[1]), (point[0], point[1])):
                is_inside = False
                break

    return is_inside


def in_polygon(point, vertices):
    """
    Checks if a point (px, py) is inside a polygon defined by a list of
    vertices forming horizontal and vertical segments using the ray casting algorithm.
    Vertices should be ordered (clockwise or counter-clockwise).
    """
    px, py = point
    num_intersections = 0
    n = len(vertices)

    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]  # Wrap around for the last edge
        x1, y1 = v1
        x2, y2 = v2

        # Check if the segment is vertical and the ray crosses it
        if x1 == x2 and min(y1, y2) < py <= max(y1, y2):
            # The ray crosses the vertical segment if the point's x is to the left of the segment
            if px < x1:
                num_intersections += 1

        # Horizontal segments are ignored by the horizontal ray

    # If the number of intersections is odd, the point is inside
    return num_intersections % 2 == 1


def plot_grid(
    points: List[Tuple[int]], other_points: List[Tuple[int]], labels: bool = False
):
    """
    Plots the boxes and their connections in a 3D space.
    """
    _, ax = plt.subplots()

    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]

    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid()

    ax.scatter(x_vals, y_vals)
    ax.invert_yaxis()

    # Point labels
    if labels:
        for i in range(len(points)):
            ax.text(
                x_vals[i],
                y_vals[i],
                f"{x_vals[i], y_vals[i]}",
            )

    # Connecting points
    for i in range(len(points) - 1):
        v1 = points[i]
        v2 = points[i + 1]
        ax.plot(
            [v1[0], v2[0]],
            [v1[1], v2[1]],
            color="green",
            alpha=0.5,
        )

    if len(other_points) > 0:
        x_vals = [p[0] for p in other_points]
        y_vals = [p[1] for p in other_points]
        ax.scatter(x_vals, y_vals)

    plt.show()


def parse_file_1() -> Set[Tuple[int]]:
    points = []
    with open(abs_file_path) as f:
        for line in f:
            points.append(tuple(map(int, line.strip().split(","))))

    return points


def parse_file_2() -> Tuple[List[List[TileType]], List[List[int]]]:
    points = []
    min_x, max_x, min_y, max_y = (
        float("inf"),
        float("-inf"),
        float("inf"),
        float("-inf"),
    )
    with open(abs_file_path) as f:
        for line in f:
            new_point = list(map(int, line.strip().split(",")))
            points.append(new_point)

            if new_point[0] < min_x:
                min_x = new_point[0]
            if new_point[0] > max_x:
                max_x = new_point[0]
            if new_point[1] < min_y:
                min_y = new_point[1]
            if new_point[1] > max_y:
                max_y = new_point[1]

    print(min_x, max_x, min_y, max_y)

    for i in range(len(points)):
        points[i] = points[i][0] - min_x, points[i][1] - min_y

    # print('here')
    # grid = [[TileType.EMPTY for _ in range(max_y - min_y + 1)] for _ in range(max_x - min_x + 1)]
    # print('here')

    # for p in points:
    #     grid[p[0]][p[1]] = TileType.TILE

    # print('here')

    return [], points


def part2_2():
    _, points = parse_file_2()
    polygon = Polygon(points)

    def area(edge) -> int:
        (x1, y1), (x2, y2) = edge
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    max_area = 0
    max_rect = None
    for edge in sorted(combinations(points, 2), key=area, reverse=True):
        (x1, y1), (x2, y2) = edge
        if polygon.contains(box(x1, y1, x2, y2)):
            a = area(edge)
            if a > max_area:
                max_area = a
                max_rect = box(x1, y1, x2, y2)
                print("Max area:", max_area)

    print("Maximum area:", max_area)
    print("Max rectangle:", max_rect)


# part2_2()
part2()
