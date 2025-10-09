import os
from typing import List
from collections import Counter
from dataclasses import dataclass


@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: int
    hand_strength: List[int]


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

cards_strength = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


"""
Read all hands
Classify the hand type (pair, two pairs...) as a number (1, 2...)
Make a modified sorting algorithm
    Sort by the hand type
    If there are two hands with same type, check stronger card
"""


def part1():
    hands = parse_file()
    hands = list(map(classify_hand, hands))

    def compare_hand(hand: Hand):
        return (
            hand.hand_type,
            hand.hand_strength[0],
            hand.hand_strength[1],
            hand.hand_strength[2],
            hand.hand_strength[3],
            hand.hand_strength[4],
        )

    hands.sort(key=compare_hand)

    total_winnings = 0
    for i, hand in enumerate(hands, 1):
        total_winnings += hand.bid * i

    print("Total winnings:", total_winnings)


def part2():
    pass


def classify_hand(hand: Hand):
    cards_count = Counter(hand.cards)

    # Number of different cards
    match len(cards_count):
        case 1:  # 5 Kind
            hand.hand_type = 6
        case 2:  # 4 Kind, Full house
            if cards_count.most_common(1)[0][1] == 4:
                # 4 Kind
                hand.hand_type = 5
            else:
                # Full house
                hand.hand_type = 4
        case 3:  # 3 Kind, 2 pairs
            if cards_count.most_common(1)[0][1] == 3:
                # 3 Kind
                hand.hand_type = 3
            else:
                # 2 pairs
                hand.hand_type = 2
        case 4:  # 1 pair
            hand.hand_type = 1
        # Defaults to 0, high card

    return hand


def parse_file() -> List[Hand]:
    hands = list()
    with open(abs_file_path) as f:
        for line in f:
            hand, bid = line.strip().split()

            hand_cards_strength = [cards_strength[card] for card in hand]
            hands.append(Hand(hand, int(bid), 0, hand_cards_strength))

    return hands


part1()
