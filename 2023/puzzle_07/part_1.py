#!/usr/bin/env python3

from collections import Counter
from sys import argv


LABEL_STRENGTH = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "J": 9,
    "T": 8,
    "9": 7,
    "8": 6,
    "7": 5,
    "6": 4,
    "5": 3,
    "4": 2,
    "3": 1,
    "2": 0
}


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)
        self._type = None

    @property
    def type(self):
        if self._type:
            return self._type

        counts = Counter(self.cards)
        values = counts.values()

        if len(counts) == 1:
            # five of a kind
            self._type = 7
        elif len(counts) == 2:
            if 4 in values:
                # four of a kind
                self._type = 6
            elif 3 in values:
                # full house
                self._type = 5
        elif 3 in values:
            # three of a kind
            self._type = 4
        elif 2 in values:
            num_pairs = 0
            for v in values:
                if v == 2:
                    num_pairs += 1
                if num_pairs == 2:
                    # two pair
                    self._type = 3
                else:
                    # one pair
                    self._type = 2
        else:
            # high card
            self._type = 1

        return self._type

    def __gt__(self, other):
        if self.type > other.type:
            return True
        if self.type == other.type:
            for a, b in zip(self.cards, other.cards):
                a_strength = LABEL_STRENGTH[a]
                b_strength = LABEL_STRENGTH[b]
                if a_strength > b_strength:
                    return True
                elif a_strength < b_strength:
                    return False
        return False

    def __repr__(self):
        return f"Hand(cards={self.cards}, bid={self.bid}, type={self._type})"


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def calculate_total_winnings(hands):
    total_winnings = 0
    sorted_hands = sorted(hands)
    for i, hand in enumerate(sorted_hands):
        rank = i + 1
        hand_winnings = rank * hand.bid
        total_winnings += hand_winnings

    return total_winnings


def parse_input_file(file_name):
    hands = []
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            cards, bid = row.split(" ")
            hands.append(Hand(cards=cards, bid=bid))

    return hands


def test_examples():
    hands = parse_input_file(r"test_input.txt")
    answer = calculate_total_winnings(hands)

    assert answer == 6440

    print("Tests passed.")


def puzzle():
    hands = parse_input_file(r"input.txt")
    answer = calculate_total_winnings(hands)

    wrong_answers = [
        250123127
    ]
    assert answer not in wrong_answers, "got the wrong answer again :("

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
