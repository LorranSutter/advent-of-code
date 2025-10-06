import os
import re
from typing import List
from dataclasses import dataclass


@dataclass
class Card:
    winning: set
    have: List[int]


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


# 135221 Too high
def part1():
    cards = read_file()

    total_points = 0
    for card in cards:
        count_winning = 0
        for num in card.have:
            if num in card.winning:
                count_winning += 1

        if count_winning > 0:
            total_points += 2**(count_winning-1)

    print("Total card points:", total_points)


def part2():
    pass

    # print("Total card points:", total_points)


def read_file() -> List[Card]:
    cards = []
    with open(abs_file_path) as f:
        for line in f:
            # Remove "Card 1:"
            line = line.rstrip("\n").split(":")
            # Separate winning and you have numbers
            line = line[1].split("|")

            winning_nums = set(re.split(r"\s+", line[0].strip()))
            have_nums = re.split(r"\s+", line[1].strip())

            cards.append(Card(winning_nums, have_nums))

    return cards


part1()
