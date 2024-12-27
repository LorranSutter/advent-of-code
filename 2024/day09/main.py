import os
from typing import List
from dataclasses import dataclass


@dataclass
class File:
    ID: int
    num_files: int


@dataclass
class Space:
    files: List[File]
    free: int


script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    disk_map = read_file()
    total_num_files = count_files(disk_map)
    file_array = build_file_array(disk_map)

    checksum = calculate_checksum_1(disk_map, file_array, total_num_files)

    print("File systeam checksum:", checksum)


def part2():
    disk_map = read_file()
    spaces = build_array(disk_map)
    compact_files(spaces)

    checksum = calculate_checksum_2(spaces)

    print("File systeam checksum:", checksum)


def read_file():
    with open(abs_file_path) as f:
        return [int(digit) for digit in f.read().rstrip("\n")]


def count_files(disk_map):
    # Iterate only over file digits
    return sum((int(digit) for digit in disk_map[::2]))


def build_file_array(disk_map):
    file_array = []
    # Iterate only over file digits
    for i, digit in enumerate(disk_map[::2]):
        file_array.extend([i for _ in range(digit)])
    return file_array


def build_array(disk_map):
    spaces = []
    for i, digit in enumerate(disk_map):
        if i % 2 == 0:
            spaces.append(Space([File(i // 2, digit)], 0))
        else:
            spaces.append(Space([File(0, 0)], digit))

    return spaces

def compact_files(spaces):    
    spaces_array_size = len(spaces)
    for i, chunk in enumerate(spaces[::-2]):
        chunk_size = chunk.files[0].num_files
        if chunk_size == 0:
            continue

        chunk_id = spaces_array_size - 2 * i - 1
        for j, space in enumerate(spaces[:chunk_id]):
            if space.free == 0:
                continue
            if space.free >= chunk_size:
                spaces[j].free -= chunk_size
                spaces[j].files.extend(chunk.files)

                spaces[chunk_id].files = [File(0, 0)]
                spaces[chunk_id].free += chunk_size

                break


def calculate_checksum_1(disk_map, file_array, total_num_files):
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


def calculate_checksum_2(spaces):
    checksum, file_counting = 0, 0
    for space in spaces:
        for file in space.files:
            for _ in range(file.num_files):
                checksum += file.ID * file_counting
                file_counting += 1
        file_counting += space.free
    
    return checksum



def print_disk(file_array, disk_array):
    res = ""
    file_array = filter(lambda item: item != "", file_array)
    for f, s in zip(file_array, disk_array):
        res += f + "." * s
    print(res)


part2()