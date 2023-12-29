#!/usr/bin/env python3

from collections import Counter
from sys import argv


LABEL_STRENGTH = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
}


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)
        self._type = None
        self._counts = None
        self._values = None

    @property
    def type(self):
        if self._type:
            return self._type

        self._type = self._determine_best_hand_type()
        log(f"    after: {self._type}")
        return self._type

    def _determine_best_hand_type(self):
        if "J" not in self.cards or self.cards == "JJJJJ":
            return self._calculate_type()

        t = self._calculate_type()
        log(f"{self.cards}")
        log(f"    before: {t}")
        num_wildcards = self._counts["J"]

        if t == 6:
            # XXXXJ => five of a kind
            return 7

        if t == 5:
            # if it's a full house, there are either 2 or 3 Js,
            # which means they can be upgraded to whatever the other label is
            return 7

        if t == 4:
            # t 4 is 3 of a kind
            if num_wildcards == 2:
                # XXXJJ => five of a kind
                return 7
            else:
                # XXXJY => 4 of a kind
                # JJJXY => 4 of a kind
                return 6

        if t == 3:
            # t 3 is two pair
            if num_wildcards == 2:
                # XXJJA => 4 of a kind
                return 6
            else:
                # XXYYJ => full house
                return 5

        if t == 2:
            # t 2 is one pair
            # JJYZA => three of a kind
            # XXYZJ => three of a kind
            return 4

        if t == 1:
            # t 1 is high card
            # ABCDJ => one pair
            return 2

        return t

    def _calculate_type(self):
        self._counts = Counter(self.cards)
        self._values = self._counts.values()

        if len(self._counts) == 1:
            # five of a kind
            return 7

        if len(self._counts) == 2:
            if 4 in self._values:
                # four of a kind
                return 6
            elif 3 in self._values:
                # full house
                return 5

        if 3 in self._values:
            # three of a kind
            return 4

        if 2 in self._values:
            num_pairs = 0
            for v in self._values:
                if v == 2:
                    num_pairs += 1
            if num_pairs == 2:
                # two pair
                return 3
            else:
                # one pair
                return 2
        # high card
        return 1

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
    """
    five of a kind = 7
    four of a kind = 6
    full house = 5
    three of a kind = 4
    two pair = 3
    one pair = 2
    high card = 1
    """
    test_hands = [
        # 4 -> 5 of a kind
        ("AAAAJ", 7),
        # full house -> 5 of a kind
        ("AAJJJ", 7),
        ("AAAJJ", 7),
        # 3 -> 4 of a kind
        ("AAAJK", 6),
        ("JJJAK", 6),
        # two pair -> full house
        ("AAKKJ", 5),
        # two pair -> 4 of a kind
        ("AAJJK", 6),
        # one pair -> 3 of a kind
        ("JJKQA", 4),
        ("KKQAJ", 4),
        # high card -> one pair
        ("AKQ9J", 2),
    ]
    for h, t in test_hands:
        hand = Hand(cards=h, bid=0)
        assert hand.type == t, f"{h}: {hand.type} != {t}"

    hands = parse_input_file(r"test_input.txt")
    answer = calculate_total_winnings(hands)

    assert answer == 5905

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
