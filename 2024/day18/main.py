import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)

size = 71 if rel_path == "input" else 7
limit = 1024 if rel_path == "input" else 12


def part1():
    start = (0, 0)
    grid = read_file(size, limit)
    adjacent_matrix = make_adjacent_matrix(grid, size)
    end, parents = BFS(adjacent_matrix, start, (size - 1, size - 1))

    steps = 0
    current = end
    while current != start:
        current = parents[current]
        steps += 1

    print("Minimum number of steps:", steps)


def part2():
    corrupted = read_file_2()
    len_corrupted = len(corrupted)
    high, low = len_corrupted, 0

    end = None
    while low <= high:
        mid = low + (high - low) // 2
        grid = make_grid(size, corrupted[:mid])
        adjacent_matrix = make_adjacent_matrix(grid, size)

        end, _ = BFS(adjacent_matrix, (0, 0), (size - 1, size - 1))

        if end:
            low = mid + 1
        else:
            high = mid - 1
    
    print("First byte to prevent exit",corrupted[mid-1])


def read_file(size, limit):
    grid = [["." for _ in range(size)] for _ in range(size)]
    with open(abs_file_path) as f:
        for count, line in enumerate(f, 1):
            i, j = list(map(int, line.rstrip("\n").split(",")))
            grid[j][i] = "#"
            if count >= limit:
                break

    return grid


def read_file_2():
    corrupted = []
    with open(abs_file_path) as f:
        for line in f:
            corrupted.append(tuple(map(int, line.rstrip("\n").split(","))))

    return corrupted


def make_adjacent_matrix(grid, size):
    adjacent_matrix = {}

    for i in range(size):
        for j in range(size):
            if grid[j][i] == ".":
                adjacent_matrix[(j, i)] = []
                if in_bounds((j + 1, i), size) and grid[j + 1][i] == ".":
                    adjacent_matrix[(j, i)].append((j + 1, i))
                if in_bounds((j - 1, i), size) and grid[j - 1][i] == ".":
                    adjacent_matrix[(j, i)].append((j - 1, i))
                if in_bounds((j, i + 1), size) and grid[j][i + 1] == ".":
                    adjacent_matrix[(j, i)].append((j, i + 1))
                if in_bounds((j, i - 1), size) and grid[j][i - 1] == ".":
                    adjacent_matrix[(j, i)].append((j, i - 1))

    return adjacent_matrix


def make_grid(size, corrupted):
    grid = [["." for _ in range(size)] for _ in range(size)]
    for c in corrupted:
        grid[c[1]][c[0]] = "#"

    return grid


def BFS(adjacent_matrix, start, end):
    Q, visited = [], []
    visited.append(start)
    Q.append(start)
    parents = {}
    while Q != []:
        v = Q.pop(0)
        if v == end:
            return v, parents
        for w in adjacent_matrix[v]:
            if w not in visited:
                visited.append(w)
                parents[w] = v
                Q.append(w)
    return None, None


def print_grid(grid):
    for i in range(len(grid)):
        print("".join(grid[i]))


def in_bounds(pos, size):
    return pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size


part2()
