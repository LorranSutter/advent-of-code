import os
import re
from typing import List
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Read each line representing a scratchcard, strip the "Card X:" prefix, and split on the vertical bar (`|`)
- Split the numbers on each side by whitespace to separate the set of winning numbers from the list of numbers we have
- Store these sets/lists using the `Card` dataclass

Part 1:
- For each card, calculate the count of numbers we have that are also in the winning numbers set
- If the card has N > 0 matches, the point value is 2^{N-1}
- Sum the points across all scratchcards and print the total

Part 2:
- Maintain an array `cards_count` initialized to 1 for each card to keep track of the total copies of each card we own
- For each card i, count how many winning matches N it has
- Add the quantity of the current card (stored in `cards_count[i]`) to the next N subsequent cards (i.e. indices i+1 to i+N)
- Sum the total quantity of cards owned (originals plus won copies) and print the total
"""


@dataclass
class Card:
    winning: set
    have: List[int]


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    cards = read_file()

    total_points = 0
    for card in cards:
        count_winning = 0
        for num in card.have:
            if num in card.winning:
                count_winning += 1

        if count_winning > 0:
            total_points += 2 ** (count_winning - 1)

    print("Total card points:", total_points)


@timer
def part2():
    cards = read_file()

    cards_count = [1 for _ in cards]
    total_cards = 0
    for i, card in enumerate(cards):
        total_cards += 1
        count_wins = 0
        for num in card.have:
            if num in card.winning:
                count_wins += 1
                cards_count[i + count_wins] += cards_count[i]
        total_cards += cards_count[i]

    print("Total cards:", total_cards)


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
part2()
