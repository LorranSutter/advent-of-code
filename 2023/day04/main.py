import os
import re
from typing import List
from dataclasses import dataclass

from utils.timer import timer


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
    """
    Create a list to keep track of how many copies of each card
    Search for how many wins in each card, count how many wins
    When a win is found, update the cards_count at the index after the current card
    The index depends on the number of wins, 1 win -> next card, 2 wins -> next 2 cards...
    The trick is how much to add to the cards_count per index
        This is the number of cards of the current index already calculated in the previous iteration
        Ex, card 1 -> 4 wins
            card 2, 3, 4 -> increases 1
            When scan card 2, we will add 2 to the next card
    """
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


part2()
