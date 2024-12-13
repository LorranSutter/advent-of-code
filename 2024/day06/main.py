import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    chart, initial_pos = read_file()
    chart[initial_pos[0]][initial_pos[1]] = "X"

    positions = walk(chart, initial_pos, (-1, 0), 1, len(chart))
    print("Distinct positions visited:", positions)


def part2():
    chart, initial_pos = read_file()

    path = walk_path(chart, initial_pos, (-1, 0), len(chart))
    total_obstacles = 0
    for pos in path:
        if pos == initial_pos:
            continue

        chart[pos[0]][pos[1]] = "#"
        total_obstacles += walk_2(chart, initial_pos, (-1, 0), len(chart))
        chart[pos[0]][pos[1]] = "."

    print("Total obstacles:", total_obstacles)


def read_file():
    chart = []
    initial_pos = None
    with open(abs_file_path) as f:
        for i, row in enumerate(f):
            row = list(map(str, row.rstrip("\n")))
            chart.append(row)
            if not initial_pos:
                for j, item in enumerate(row):
                    if item == "^":
                        initial_pos = (i, j)
    return chart, initial_pos


def walk(chart, pos, direction, count, size):
    while in_bounds(pos, size):

        if chart[pos[0]][pos[1]] == "#":
            return walk(
                chart,
                sub(pos, direction),
                rotate(direction),
                count,
                size,
            )
        elif chart[pos[0]][pos[1]] != "X":
            count += 1
            chart[pos[0]][pos[1]] = "X"

        pos = add(pos, direction)

    return count


def walk_path(chart, pos, direction, size):
    path = []
    while in_bounds(pos, size):

        if chart[pos[0]][pos[1]] == "#":
            pos = sub(pos, direction)
            direction = rotate(direction)
        elif pos not in path:
            path.append(pos)

        pos = add(pos, direction)

    return path


def walk_2(chart, pos, direction, size):
    visited = []
    while in_bounds(pos, size):

        if chart[pos[0]][pos[1]] == "#":
            if (pos, direction) not in visited:
                visited.append((pos, direction))
            else:
                return 1

            pos = sub(pos, direction)
            direction = rotate(direction)

        else:
            pos = add(pos, direction)

    return 0


def in_bounds(pos, size):
    return pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size


def rotate(v):
    return [v[1], -v[0]]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def print_chart(chart):
    for row in chart:
        print("".join(row))


part2()
