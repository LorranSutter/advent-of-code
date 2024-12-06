import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


# def firstApproach():
#     obstruction_pos = []
#     guard_pos = []
#     with open(abs_file_path) as f:
#         for i, row in enumerate(f):
#             for j, item in enumerate(row.rstrip("\n")):
#                 if item == "#":
#                     obstruction_pos.append([i, j])
#                 elif item == "^":
#                     guard_pos = [i, j]

#     print("Distinct positions visited:")


def part1():
    chart = []
    initial_pos = None
    with open(abs_file_path) as f:
        for i, row in enumerate(f):
            row = list(map(str, row.rstrip("\n")))
            chart.append(row)
            if not initial_pos:
                for j, item in enumerate(row):
                    if item == "^":
                        initial_pos = [i, j]
                        chart[i][j] = "X"

    positions = walk(chart, initial_pos, [-1, 0], 1, len(chart))
    print("Distinct positions visited:", positions)


def part2():
    with open(abs_file_path) as f:
        for row in f:
            pass

    print("Distinct positions visited:")


def walk(chart, pos, direction, count, size):
    while in_bounds(pos[0], pos[1], size):

        if chart[pos[0]][pos[1]] == "#":
            return walk(
                chart,
                [pos[0] - direction[0], pos[1] - direction[1]],
                rotate(direction),
                count,
                size,
            )
        elif chart[pos[0]][pos[1]] != "X":
            count += 1
            chart[pos[0]][pos[1]] = "X"

        pos[0], pos[1] = pos[0] + direction[0], pos[1] + direction[1]

    return count


def in_bounds(posX, posY, size):
    return posX >= 0 and posX < size and posY >= 0 and posY < size


def rotate(v):
    return [v[1], -v[0]]


part1()
