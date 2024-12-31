import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    locks, keys = read_file(5)

    print(keys)
    for lock in locks:
        print(lock)

    for key in keys:
        print(key)

    print(fit(locks, keys, 5))


def part2():
    pass


def read_file(size: int):
    locks, keys = [], []
    with open(abs_file_path) as f:
        schematics = f.read().split("\n\n")

        for schematic in schematics:
            schematic = schematic.split("\n")
            
            heights = [-1 for _ in range(size)]
            for line in schematic:
                for i in range(size):
                    if line[i] == "#":
                        heights[i] += 1

            if schematic[0] == "#" * size:
                locks.append(heights)
            else:
                keys.append(heights)

    return locks, keys


def fit(locks, keys, size):
    total_fits = 0
    for lock in locks:
        for key in keys:
            fits = True
            for i in range(size):
                if lock[i] + key[i] > size:
                    fits = False
                    break
            if fits:
                total_fits += 1

    return total_fits


part1()
