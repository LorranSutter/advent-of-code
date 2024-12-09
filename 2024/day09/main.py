import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    disk_map = read_file()
    total_num_files = count_files(disk_map)
    file_array = build_file_array(disk_map)

    checksum = calculate_checksum(disk_map, file_array, total_num_files)

    print("File systeam checksum:", checksum)


def part2():
    print("File systeam checksum:")


def read_file():
    with open(abs_file_path) as f:
        return [int(digit) for digit in f.read().rstrip("\n")]


def count_files(disk_map):
    return sum((int(digit) for digit in disk_map[::2]))


def build_file_array(disk_map):
    file_array = []
    for i, digit in enumerate(disk_map[::2]):
        file_array.extend([i for _ in range(digit)])
    return file_array


def calculate_checksum(disk_map, file_array, total_num_files):
    """
    00...111...2...333.44.5555.6666.777.888899
    |                                        |
    head                                  tail
    """

    head = 0
    tail = len(file_array) - 1
    pointer = head
    direction, checksum, file_counting = 1, 0, 0
    for digit in disk_map:
        for _ in range(int(digit)):
            checksum += file_array[pointer] * file_counting
            pointer += 1 * direction
            file_counting += 1
            if file_counting >= total_num_files:
                return checksum

        if direction == 1:
            head = pointer
            pointer = tail
        else:
            tail = pointer
            pointer = head
        direction *= -1


part1()
