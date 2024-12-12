import os
import math

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    arr = read_file()

    temp = []
    for _ in range(25):
        for i in range(len(arr)):
            if arr[i] == 0:
                temp.append(1)
            else:
                size = math.floor(math.log10(arr[i])) + 1
                if size % 2 == 0:
                    middle = 10 ** (size // 2)
                    stone1 = arr[i] // middle
                    stone2 = arr[i] % middle
                    temp.extend([stone1, stone2])
                else:
                    temp.append(arr[i] * 2024)
        arr = temp.copy()
        temp = []

    print("Total stones:", len(arr))


def part2():
    arr = read_file()

    print("Total stones:", len(arr))


def read_file():
    with open(abs_file_path) as f:
        return list(map(int, f.read().rstrip("\n").split()))


part1()
