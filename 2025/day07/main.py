import os
from enum import Enum
from typing import List

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Preprocessing:
- We convert the characters to numbers, to help with the iterations:
    - "." -> 0 (empty)
    - "S" -> 1 (initial beam)
    - "^" -> 2 (split)

Part 1:
- We iterate through each line of the grid and each cell.
- If we find an empty cell
  - If the cell above is a beam, we mark the current cell as a beam as well
- If we find a split cell
  - If the cell above is a beam, we mark the adjacent left and right cells as beams
  - We also increment the split counter
- Finally, we print the total number of splits

Part 2:
- We pretty much do the same as part 1, but we also keep track of the timelines
- The timelines is an array of the length of the width of the grid
- The only difference here is when we reach a split
    - The left and right timelines get the value of the current timeline added to them
    - The current timeline gets set to 0
- The total of timelines is the sum of the timelines array at the end of the iterations

Example:
Grid:                      [.  .  |  .  .]
Current timelines:         [0, 0, 2, 0, 0]
Grid:                      [.  .  ^  .  .]
After split in the middle: [0, 2, 0, 2, 0]
Grid:                      [.  ^  .  ^  .]
After splits:              [2, 0, 4, 0, 2]
Total timelines:           8

Note: For part2, a DFS would also work, but this approach is simpler.
"""


class Diagram_map(Enum):
    EMPTY = 0
    BEAM = 1
    SPLIT = 2


diagram_to_num = {
    ".": Diagram_map.EMPTY,
    "S": Diagram_map.BEAM,
    "^": Diagram_map.SPLIT,
}


def part1():
    grid = parse_file()

    splits = 0
    for i in range(1, len(grid)):
        for j in range(len(grid[1])):
            if grid[i][j] == Diagram_map.EMPTY and grid[i - 1][j] == Diagram_map.BEAM:
                grid[i][j] = Diagram_map.BEAM
            elif grid[i][j] == Diagram_map.SPLIT and grid[i - 1][j] == Diagram_map.BEAM:
                splits += 1
                grid[i][j - 1] = Diagram_map.BEAM
                grid[i][j + 1] = Diagram_map.BEAM

    print("Total splits:", splits)


def part2():
    grid = parse_file()

    timelines = grid[0].copy()
    for i in range(len(timelines)):
        if isinstance(timelines[i], Diagram_map):
            timelines[i] = timelines[i].value

    for i in range(1, len(grid)):
        for j in range(len(grid[1])):
            if grid[i][j] == Diagram_map.EMPTY and grid[i - 1][j] == Diagram_map.BEAM:
                grid[i][j] = Diagram_map.BEAM
            elif grid[i][j] == Diagram_map.SPLIT and grid[i - 1][j] == Diagram_map.BEAM:
                grid[i][j - 1] = Diagram_map.BEAM
                grid[i][j + 1] = Diagram_map.BEAM
                timelines[j - 1] += timelines[j]
                timelines[j + 1] += timelines[j]
                timelines[j] -= timelines[j]

    print("Total timelines:", sum(timelines))


def parse_file() -> List[List[str]]:
    grid = []
    with open(abs_file_path) as f:
        for line in f:
            line = [diagram_to_num[char] for char in line.strip()]
            grid.append(line)

    return grid


part2()
