import os

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
                size = len(str(arr[i]))
                if size % 2 == 0:
                    stone1 = int(str(arr[i])[: size // 2])
                    stone2 = int(str(arr[i])[size // 2 :])
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
