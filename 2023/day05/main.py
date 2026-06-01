import os
import math
from typing import List, Tuple
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into two structures:
  1. A tuple of seed numbers
  2. A list of category maps, where each category contains a list of Maps dataclasses
- Each Map stores the destination range start, source range start, and calculates the end positions

Part 1:
- Iterate over each individual seed number, treating it as the initial location
- For each seed, traverse through all category maps in sequence (seed→soil→fertilizer→...→location)
- Within each category, check if the current location falls within any mapping range
- If a match is found, calculate the new location using: new_location = current_location - srcInit + destInit
- If no match is found, the location remains unchanged (identity mapping)
- Track the minimum location value across all seeds and output it at the end

Part 2:
- Similar to Part 1, but now seeds are interpreted as ranges: [start, start + length - 1]
- Instead of checking individual numbers, we work with range intersections
- For each seed range, we check how it intersects with each mapping range in the category
- Three intersection scenarios can occur:
  
  Scenario 1 - No overlap:
    Seed range: [10, 20] 10 ---------- 20
    Map range:  [25, 35]                      25 ----- 30
    Result: No intersection, try next mapping
  
  Scenario 2 - Complete overlap
    Seed range: [15, 25]         15 ---- 25
    Map range:  [10, 30] 10 -------------------- 30
    Result: Entire seed range maps to destination
  
  Scenario 3 - Partial overlap (the tricky case):
    Seed range: [10, 30] 10 -------------------- 30
    Map range:  [15, 25]         15 ----- 25
    Result: Split into three parts:
      - before_overlap: [10, 15] → stays unmapped, needs further checking
      - overlap: [15, 25] → maps to destination
      - after_overlap: [25, 30] → stays unmapped, needs further checking

- When partial overlaps occur, we "split" the seed range into multiple sub-ranges
- The overlapping portion is immediately mapped to the destination category
- The non-overlapping portions (before/after) are added back to the queue to be checked against remaining mappings
- This process continues until all sub-ranges have been tested against all mappings in the current category
- We then repeat for each subsequent category (soil→fertilizer→water→...→location)
- Finally, track the minimum starting location across all resulting ranges and output it
"""


@dataclass
class Maps:
    destInit: int
    destEnd: int
    srcInit: int
    srcEnd: int


@dataclass
class Category:
    maps: List[Maps]


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    seeds, categorie_maps = parse_file()
    lowest = math.inf

    for seed in seeds:
        location = seed
        for category_map in categorie_maps:
            for mapping in category_map:
                if mapping.srcInit <= location <= mapping.srcEnd:
                    location = location - mapping.srcInit + mapping.destInit
                    break

        if location < lowest:
            lowest = location

    print(f"Lowest location number: {lowest}")


@timer
def part2():
    seeds, categorie_maps = parse_file()

    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append([seeds[i], seeds[i] + seeds[i + 1] - 1])

    lowest = math.inf

    for seed_range in seed_ranges:
        locations = [seed_range]
        for category_map in categorie_maps:
            new_locations = []
            for location in locations:
                new_locations.extend(map_location(location, category_map))
            locations = new_locations.copy()

        for location in locations:
            if location[0] < lowest:
                lowest = location[0]

    print(f"Lowest location number: {lowest}")


def map_location(location: List[int], category_mappings: List[Maps]) -> List[List[int]]:
    locations_to_map = [location]
    next_locations = []

    while locations_to_map:
        current_location = locations_to_map.pop()
        for mapping in category_mappings:
            before_overlap, overlap, after_overlap = range_intersection(
                current_location[0],
                current_location[1],
                mapping.srcInit,
                mapping.srcEnd,
            )
            if before_overlap:
                # Seeds out of the overlap that passes to the next category
                locations_to_map.append(before_overlap)
            if after_overlap:
                # Seeds out of the overlap that passes to the next category
                locations_to_map.append(after_overlap)
            if overlap:
                # All seeds here pass to the next category
                next_locations.append(
                    [
                        overlap[0] - mapping.srcInit + mapping.destInit,
                        overlap[1] - mapping.srcInit + mapping.destInit,
                    ]
                )
                current_location = None
                break

        if current_location:
            # Seeds that didn't match any mapping
            next_locations.append(current_location)

    return next_locations


def range_intersection(
    a_start: int, a_end: int, b_start: int, b_end: int
) -> Tuple[List[int], List[int], List[int]]:
    before_overlap, overlap, after_overlap = None, None, None

    if a_end <= b_start or b_end <= a_start:  # no overlap
        return None, None, None

    if a_start < b_start:  # split original interval at b_start
        before_overlap = [a_start, b_start]
        a_start = b_start

    if b_end < a_end:  # split original interval at b_end
        after_overlap = [b_end, a_end]
        a_end = b_end

    overlap = [a_start, a_end]

    return before_overlap, overlap, after_overlap


def parse_file() -> Tuple[Tuple[int], List[Category]]:
    with open(abs_file_path) as f:
        file = f.read().split("\n\n")

    # Remove 'seeds:'
    seeds = file[0].strip().split(":")
    seeds = tuple(map(int, seeds[1].split()))

    # Parse each category
    categorie_maps = []
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
                srcEnd=new_map[1] + new_map[2] - 1
            )
            new_maps.append(new_map)

        categorie_maps.append(new_maps)

    return seeds, categorie_maps


part1()
part2()
