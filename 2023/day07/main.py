import os
from typing import List
from collections import Counter
from dataclasses import dataclass


@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: int


script_dir = os.path.dirname(__file__)
rel_path = "input_sample.txt"
abs_file_path = os.path.join(script_dir, rel_path)


"""
Read all hands
Classify the hand type (pair, two pairs...) as a number (1, 2...)
Make a modified sorting algorithm
    Sort by the hand type
    If there are two hands with same type, check stronger card
"""


def part1():
    hands = parse_file()
    hands = map(classify_hand, hands)

    for hand in hands:
        print(hand)


def part2():
    pass

def classify_hand(hand: Hand):
    cards_count = Counter(hand.cards)

    # Number of different cards
    match len(cards_count):
        case 1: # 5 Kind
            hand.hand_type = 6
        case 2: # 4 Kind, Full house
            if cards_count.most_common(1)[0][1] == 4:
                # 4 Kind
                hand.hand_type = 5
            else:
                # Full house
                hand.hand_type = 4
        case 3: # 3 Kind, 2 pairs
            if cards_count.most_common(1)[0][1] == 3:
                # 3 Kind
                hand.hand_type = 3
            else:
                # 2 pairs
                hand.hand_type = 2
        case 4: # 1 pair
            hand.hand_type = 1
        # Defaults to 0, high card
    
    return hand

def parse_file() -> List[Hand]:
    hands = list()
    with open(abs_file_path) as f:
        for line in f:
            hand, bid = line.strip().split()
            hands.append(Hand(hand, int(bid), 0))

    return hands


part1()
