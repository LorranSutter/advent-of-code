import os
import re

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)

size_input = (103, 101)
size_sample = (7, 11)


def part1():
    seconds = 100
    size = size_input if rel_path == "input" else size_sample
    positions, velocities = read_file()

    quadrant_count = [0, 0, 0, 0]
    for i in range(len(positions)):
        positions[i] = mod(add(positions[i], mul(seconds, velocities[i])), size)
        quadrant_id = get_quadrant(positions[i], size)

        if quadrant_id != None:
            quadrant_count[quadrant_id] += 1

    safety_factor = (
        quadrant_count[0] * quadrant_count[1] * quadrant_count[2] * quadrant_count[3]
    )

    print("Safety factor:", safety_factor)


def part2():

    print("Safety factor:")


def read_file():
    pattern = r"p=(\d+),(\d+)\sv=(-?\d+),(-?\d+)"

    positions = []
    velocities = []
    with open(abs_file_path) as f:
        for line in f:
            items = re.findall(pattern, line)[0]
            positions.append((int(items[1]), int(items[0])))
            velocities.append((int(items[3]), int(items[2])))

    return positions, velocities


def print_grid(size, positions):
    grid = [["." for _ in range(size[1])] for _ in range(size[0])]

    for p in positions:
        if grid[p[0]][p[1]] == ".":
            grid[p[0]][p[1]] = "1"
        else:
            grid[p[0]][p[1]] = str(int(grid[p[0]][p[1]]) + 1)

    for i in range(size[0]):
        print("".join(grid[i]))


def get_quadrant(p, size):
    middle_x = size[0] // 2
    middle_y = size[1] // 2

    if in_quadrant(p, 0, middle_x - 1, 0, middle_y - 1):
        return 0
    if in_quadrant(p, 0, middle_x - 1, middle_y + 1, size[1]):
        return 1
    if in_quadrant(p, middle_x + 1, size[0], 0, middle_y - 1):
        return 2
    if in_quadrant(p, middle_x + 1, size[0], middle_y + 1, size[1]):
        return 3


def in_quadrant(p, x0, x1, y0, y1):
    return p[0] >= x0 and p[0] <= x1 and p[1] >= y0 and p[1] <= y1


def mul(a, v):
    return (a * v[0], a * v[1])


def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def mod(v1, v2):
    return (v1[0] % v2[0], v1[1] % v2[1])


part1()
