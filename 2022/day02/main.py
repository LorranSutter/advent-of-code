import os
from typing import List, Tuple

from utils.timer import timer

"""
Part 1:
- The `plays` table does all the work: `plays[opponent][me]` holds the *full* round score for that matchup, i.e. the
  shape value we picked (1/2/3) plus the outcome bonus (0 lose / 3 draw / 6 win) already added together. So once we
  know both shapes, scoring a round is a single lookup and the whole answer is a sum over the rounds.
- The one snag is that our second column arrives as X/Y/Z while the table is keyed by A/B/C. Both triples are
  consecutive in ASCII and sit exactly 23 apart, so we can rewrite each letter instead of branching on it:

    ord("X") - ord("A") = 88 - 65 = 23   ->   chr(ord("X") - 23) == "A",  "Y" -> "B",  "Z" -> "C"

  After the shift, sum `plays[c1][c2]` over every round.

Part 2:
- Same `plays` table, but the second column is now the outcome we need, not the shape we play. So we first work
  backwards to our shape from the opponent's shape plus the target result, then look the score up as before.
- Two little maps make that step trivial: `wins[c1]` is the shape that beats `c1` (what we play to win), and
  `losts[c1]` is the shape `c1` beats (what we play to lose). A draw is just playing `c1` itself.
- So X (lose) -> plays[c1][losts[c1]], Y (draw) -> plays[c1][c1], Z (win) -> plays[c1][wins[c1]]. For example, an
  opponent Paper (B) with a required loss (X): losts["B"] == "A" (Rock), and plays["B"]["A"] == 1, matching the
  puzzle's 1 + 0.
"""

# Rock     A X 1
# Paper    B Y 2
# Scissors C Z 3
plays = {
    "A": {"A": 4, "B": 8, "C": 3},
    "B": {"A": 1, "B": 5, "C": 9},
    "C": {"A": 7, "B": 2, "C": 6},
}


@timer
def part1():
    column1, column2 = parse_file("input.txt")

    column2 = [chr(ord(c2) - 23) for c2 in column2]
    score = sum(plays[c1][c2] for c1, c2 in zip(column1, column2))

    print(f"Total score: {score}")


@timer
def part2():
    column1, column2 = parse_file("input.txt")

    wins = {"A": "B", "B": "C", "C": "A"}
    losts = {"B": "A", "C": "B", "A": "C"}

    score = 0
    for c1, c2 in zip(column1, column2):
        match c2:
            case "X":
                score += plays[c1][losts[c1]]
            case "Y":
                score += plays[c1][c1]
            case "Z":
                score += plays[c1][wins[c1]]

    print(f"Total score: {score}")


def parse_file(file_name: str) -> Tuple[List[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    column1, column2 = [], []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = line.strip().split(" ")
            column1.append(line[0])
            column2.append(line[1])
    return column1, column2


part1()
part2()
