import os

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    left, right = [], []
    with open(abs_file_path) as f:
        for line in f:
            line = list(map(int, line.split()))
            left.append(line[0])
            right.append(line[1])

        left.sort()
        right.sort()

        s = 0
        for l, r in zip(left, right):
            s += abs(l - r)

        print("Total distance: ", s)


@timer
def part2():
    left = []
    count_right = {}
    with open(abs_file_path) as f:
        for line in f:
            line = list(map(int, line.split()))
            left.append(line[0])

            if line[1] not in count_right:
                count_right[line[1]] = 1
            else:
                count_right[line[1]] += 1

        s = 0
        for l in left:
            if l in count_right:
                s += l * count_right[l]

        print("Similarity score: ", s)


part2()
