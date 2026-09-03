import os
import re
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- The input comes in two blocks separated by a blank line: the ASCII drawing of the stacks on top, and the list
  of moves below. We split on "\n\n" to get the two halves.
- Parsing the drawing is the fiddly part. A crate letter always sits at the same column in every row, so rather
  than hard-code the spacing we take the last line of the drawing (the label line " 1   2   3 ") and record the
  column index of every non-space character. Those indices are exactly where a crate letter would appear in the
  rows above:

      " 1   2   3 "     <- label line (last row of the drawing)
        ^   ^   ^
        1   5   9       <- column indices we record; crate letters sit here in every row above

- We then read the crate rows from the bottom up (reversed) and, for each row, pick out the character at each of
  those columns. Reading bottom-up means the first crate appended to a stack is the bottom one, so stack[-1] is
  always the top crate — which is all either part cares about.
- Each move line "move 3 from 1 to 2" becomes the tuple (3, 1, 2) by pulling every run of digits out with a
  regex. Stack numbers are 1-based, so the code subtracts 1 wherever it indexes.

Part 1:
- The crane moves crates one at a time, so moving a group of them flips their order. We model that directly: 
  for each move, pop from the source stack and append to the destination, num times. Since pop() takes the 
  current top crate and append() drops it on the new top, a run of pops-then-appends comes out reversed.
- Once every move is done, the answer is the top crate of each stack (stack[-1]) joined into a string.

Part 2:
- Same as part 1, but the crane lifts the whole group at once, so the moved crates keep their order. Instead of 
  the pop loop we take the top num crates as a slice, stacks[s1][-num:], drop them from the source with 
  stacks[s1][:-num], and extend the destination with that slice unchanged.
- The final top-crate readout is identical to part 1.
"""


@timer
def part1():
    stacks, moves = parse_file("input.txt")

    for num, s1, s2 in moves:
        for _ in range(num):
            stacks[s2 - 1].append(stacks[s1 - 1].pop())

    creates = "".join(s[-1] for s in stacks)
    print(f"Creates on top: {creates}")


@timer
def part2():
    stacks, moves = parse_file("input.txt")

    for num, s1, s2 in moves:
        crates = stacks[s1 - 1][-num:]
        stacks[s1 - 1] = stacks[s1 - 1][:-num]
        stacks[s2 - 1].extend(crates)

    creates = "".join(s[-1] for s in stacks)
    print(f"Creates on top: {creates}")


def parse_file(file_name: str) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        stacks_raw, moves_raw = f.read().split("\n\n")

    *crate_lines, label_line = stacks_raw.split("\n")

    # The label line (" 1   2   3 ") gives us the column index of each stack.
    stacks: List[List[str]] = [[] for _ in label_line.split()]
    positions = [i for i, ch in enumerate(label_line) if ch != " "]

    # Read crate rows bottom-up so stack[-1] ends up as the top crate.
    for line in reversed(crate_lines):
        for stack, col in zip(stacks, positions):
            if col < len(line) and line[col] != " ":
                stack.append(line[col])

    moves = [
        tuple(map(int, re.findall(r"\d+", line))) for line in moves_raw.splitlines()
    ]

    return stacks, moves


part1()
part2()
