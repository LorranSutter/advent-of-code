import os
import math
from typing import List, Tuple
from dataclasses import dataclass


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
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    seeds, categories = parse_file()
    lowest = math.inf

    for seed in seeds:
        location = seed
        for category in categories:
            for mapping in category.maps:
                if mapping.srcInit <= location <= mapping.srcEnd:
                    location = location-mapping.srcInit + mapping.destInit
                    break
            
        if location < lowest:
            lowest = location

    print("Lowest location number:", lowest)


def part2():
    pass


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
                destEnd=new_map[0]+new_map[2]-1,
                srcInit=new_map[1],
                srcEnd=new_map[1]+new_map[2]-1,
                rangeLength=new_map[2]
            )
            new_maps.append(new_map)

        categories.append(Category(new_maps))

    return seeds, categories


def read_file() -> List[str]:
    file = []
    with open(abs_file_path) as f:
        file = f.read().split("\n\n")

    return file


part1()
