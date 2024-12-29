import os

script_dir = os.path.dirname(__file__)
rel_path = "input_sample"
abs_file_path = os.path.join(script_dir, rel_path)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def part1():
    grid, start, end = read_file()

    path = make_path(grid, start, end)
    num_lt_min_save = cheat(grid, path, 100)

    print("Number of cheats less than minimum:", num_lt_min_save)


def part2():
    grid, start, end = read_file()

    path = make_path(grid, start, end)
    num_lt_min_save = cheat_2(path, 20, 50)

    print("Number of cheats less than minimum:", num_lt_min_save)


def read_file():
    start, end = (), ()
    grid = []
    with open(abs_file_path) as f:
        for i, line in enumerate(f):
            line = [item for item in line.rstrip("\n")]
            grid.append(line)
            for j, item in enumerate(line):
                if item == "S":
                    start = (i, j)
                    grid[i][j] = "."
                elif item == "E":
                    end = (i, j)
                    grid[i][j] = "."

    return grid, start, end


def make_path(grid, start, end):
    path = [start]
    while path[-1] != end:
        x, y = path[-1][0], path[-1][1]

        if grid[x + 1][y] == "." and (x + 1, y) not in path:
            path.append((x + 1, y))
            continue
        if grid[x - 1][y] == "." and (x - 1, y) not in path:
            path.append((x - 1, y))
            continue
        if grid[x][y + 1] == "." and (x, y + 1) not in path:
            path.append((x, y + 1))
            continue
        if grid[x][y - 1] == "." and (x, y - 1) not in path:
            path.append((x, y - 1))
            continue

        path.append((x, y))

    return path


def cheat(grid, path, min_save):
    num_lt_min_save = 0
    size = len(grid)
    path_size = len(path) - 1  # Don't count start
    for i, p in enumerate(path):
        x, y = p
        new_path_size = path_size

        if x > 1 and grid[x - 1][y] == "#" and grid[x - 2][y] == ".":
            new_init = path.index((x - 2, y))
            until_end = len(path[new_init:])
            new_path_size = i + until_end + 1

            if path_size - new_path_size >= min_save:
                num_lt_min_save += 1

        if x < size - 2 and grid[x + 1][y] == "#" and grid[x + 2][y] == ".":
            new_init = path.index((x + 2, y))
            until_end = len(path[new_init:])
            new_path_size = i + until_end + 1

            if path_size - new_path_size >= min_save:
                num_lt_min_save += 1

        if y > 1 and grid[x][y - 1] == "#" and grid[x][y - 2] == ".":
            new_init = path.index((x, y - 2))
            until_end = len(path[new_init:])
            new_path_size = i + until_end + 1

            if path_size - new_path_size >= min_save:
                num_lt_min_save += 1

        if y < size - 2 and grid[x][y + 1] == "#" and grid[x][y + 2] == ".":
            new_init = path.index((x, y + 2))
            until_end = len(path[new_init:])
            new_path_size = i + until_end + 1

            if path_size - new_path_size >= min_save:
                num_lt_min_save += 1

    return num_lt_min_save


def cheat_2(path, pico_sec, min_save):
    num_lt_min_save = 0
    path_size = len(path)
    for i, p in enumerate(path):
        for j, start_to_end in enumerate(path[i + 1 :]):
            cheat_path_dist = abs(start_to_end[0] - p[0]) + abs(start_to_end[1] - p[1])
            if cheat_path_dist <= pico_sec:
                new_path_dist = i + cheat_path_dist + len(path[i + 1 + j :])
                if path_size - new_path_dist >= min_save:
                    num_lt_min_save += 1

    return num_lt_min_save


def print_grid(grid):
    for i in range(len(grid)):
        print("".join(grid[i]))


def print_grid_with_path(grid, path, p):
    for i in range(len(grid)):
        line = ""
        for j in range(len(grid)):
            if (i, j) == p:
                line += f"{bcolors.FAIL}O{bcolors.ENDC}"
            elif (i, j) in path:
                line += f"{bcolors.OKGREEN}.{bcolors.ENDC}"
            else:
                line += grid[i][j]
        print(line)


part2()
