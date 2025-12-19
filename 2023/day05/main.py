import os
import math
from typing import List, Tuple
from dataclasses import dataclass

from utils.timer import timer


@dataclass
class Maps:
    destInit: int
    destEnd: int
    srcInit: int
    srcEnd: int
    rangeLength: int


@dataclass
class Category:
    maps: List[Maps]


script_dir = os.path.dirname(__file__)
rel_path = "input_sample.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    seeds, categories = parse_file()
    lowest = math.inf

    for seed in seeds:
        location = seed
        for category in categories:
            for mapping in category.maps:
                if mapping.srcInit <= location <= mapping.srcEnd:
                    location = location - mapping.srcInit + mapping.destInit
                    break

        if location < lowest:
            lowest = location

    print("Lowest location number:", lowest)


# 324930166 Too high
# 262615889 Too high
@timer
def part2():
    seeds, categories = parse_file()

    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append([seeds[i], seeds[i] + seeds[i + 1] - 1])
    print(seed_ranges)

    lowest = math.inf

    for seed_range in seed_ranges:
        location_range = seed_range
        for category in categories:
            for mapping in category.maps:
                print(location_range, mapping.srcInit, mapping.srcEnd)
                intersection = range_intersection(
                    location_range[0],
                    location_range[1],
                    mapping.srcInit,
                    mapping.srcEnd,
                )
                print("intersection", intersection)
                if intersection:
                    # location_range = intersection
                    new_location = [0, 0]
                    new_location[0] = (
                        intersection[0] - mapping.srcInit + mapping.destInit
                    )
                    new_location[1] = (
                        intersection[1] - mapping.srcInit + mapping.destInit
                    )

                    if (
                        new_location[1] - new_location[0]
                        > location_range[1] - location_range[0]
                    ):
                        location_range = new_location
                # if mapping.srcInit <= location_range <= mapping.srcEnd:
                #     location_range = location_range - mapping.srcInit + mapping.destInit
                #     break
            print("new location range:", location_range)

        print("final location range:", location_range)
        print()
        if location_range[0] < lowest:
            lowest = location_range[0]

    print("Lowest location number:", lowest)


def range_intersection(
    range_a_start: int, range_a_end: int, range_b_start: int, range_b_end: int
):
    intersect_start = max(range_a_start, range_b_start)
    intersect_end = min(range_a_end, range_b_end)

    if intersect_start <= intersect_end:
        return [intersect_start, intersect_end]
        # return [range_b_start - range_a_start, range_b_end - range_a_end]
    return None


def parse_file() -> Tuple[Tuple[int], List[Category]]:
    file = read_file()

    # Remove 'seeds:'
    seeds = file[0].strip().split(":")
    seeds = tuple(map(int, seeds[1].split()))

    # Parse each category
    categories = []
    for entry in file[1:]:
        entry = entry.split("\n")

        # Ignore 'category-to-category:'
        new_maps = []
        for maps in entry[1:]:
            new_map = tuple(map(int, maps.split()))
            new_map = Maps(
                destInit=new_map[0],
                destEnd=new_map[0] + new_map[2] - 1,
                srcInit=new_map[1],
                srcEnd=new_map[1] + new_map[2] - 1,
                rangeLength=new_map[2],
            )
            new_maps.append(new_map)

        categories.append(Category(new_maps))

    return seeds, categories


def read_file() -> List[str]:
    file = []
    with open(abs_file_path) as f:
        file = f.read().split("\n\n")

    return file


part2()
