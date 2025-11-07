import os
import math
import collections

script_dir = os.path.dirname(__file__)
rel_path = "input_sample"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    arr = read_file()

    temp = []
    for _ in range(40):
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
    known_stones = collections.defaultdict(lambda: None)
    known_stones[0] = [1]
    known_stones[1] = [2024]

    temp = []
    for it in range(45):
        # print(it, len(arr))
        for stone in arr:
            # print(known_stones)
            if known_stones[stone]:
                # print(stone,known_stones[stone],'here1')
                temp.extend(known_stones[stone])
            else:
                size = math.floor(math.log10(stone)) + 1
                if size % 2 == 0:
                    # print(stone,known_stones[stone],'here2')
                    middle = 10 ** (size // 2)
                    new_stones = [stone // middle, stone % middle]
                    temp.extend(new_stones)
                    known_stones[stone] = new_stones
                else:
                    # print(stone,known_stones[stone],'here3')
                    new_stone = stone * 2024
                    temp.append(new_stone)
                    known_stones[stone] = [new_stone]
            # print(temp)
            # print()
        arr = temp.copy()
        temp = []

    # print(arr)
    print("Total stones:", len(arr))


def part2_2():
    arr = read_file()
    known_stones = collections.defaultdict(lambda: None)
    known_stones[0] = [1]
    known_stones[1] = [2024]

    total = 0
    for stone in arr:
        total += get_blinked_stones(known_stones, stone, 50, total)

    # print(arr)
    print("Total stones:", total)


def get_blinked_stones(known_stones, stone, num_blinks, count):
    if num_blinks < 1:
        return count + 1

    # print(known_stones, stone)
    if known_stones[stone]:
        # print(stone, known_stones[stone], "here1")
        for stone_ in known_stones[stone]:
            count += get_blinked_stones(known_stones, stone_, num_blinks - 1, count)
    else:
        size = math.floor(math.log10(stone)) + 1
        if size % 2 == 0:
            # print(stone, known_stones[stone], "here2")
            middle = 10 ** (size // 2)
            new_stones = [stone // middle, stone % middle]
            known_stones[stone] = new_stones
            count += get_blinked_stones(
                known_stones,
                new_stones[0],
                num_blinks - 1,
                count,
            ) + get_blinked_stones(
                known_stones,
                new_stones[1],
                num_blinks - 1,
                count,
            )
        else:
            # print(stone, known_stones[stone], "here3")
            new_stone = stone * 2024
            known_stones[stone] = [new_stone]
            count += get_blinked_stones(known_stones, new_stone, num_blinks - 1, count)
    return count


def read_file():
    with open(abs_file_path) as f:
        return list(map(int, f.read().rstrip("\n").split()))


part1_optimized()
