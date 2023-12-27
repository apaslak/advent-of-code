#!/usr/bin/env python3

from collections import defaultdict
from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def extract_numbers_from_card(card):
    _, numbers = card.split(":")
    winning_numbers, your_numbers = numbers.split("|")
    winning_numbers = set(filter(None, winning_numbers.strip().split(" ")))
    your_numbers = set(filter(None, your_numbers.strip().split(" ")))

    return winning_numbers, your_numbers


def card_id(card):
    card_idx, _ = card.split(":")
    return int(card_idx.split(" ")[-1])


def process_card(card):
    card_idx = card_id(card)
    duplicate_cards = []

    winning_numbers, your_numbers = extract_numbers_from_card(card)
    matched_numbers = len(your_numbers) - len(your_numbers - winning_numbers)

    if matched_numbers:
        duplicate_cards = list(range(card_idx+1, card_idx+matched_numbers+1))
    return card_idx, duplicate_cards


def expand_duplicates(cards):
    seen = defaultdict(int)
    for key in list(cards.keys())[::-1]:
        dupes = cards[key]
        if dupes:
            for dupe in dupes:
                seen[key] = seen[key] + seen[dupe]
                log(f"key: {key}, seen[{key}]: {seen[key]}")
        seen[key] = seen[key] + 1
        log(f"key: {key}, seen[{key}]: {seen[key]}")
    return seen


def test_examples():
    cards = {}
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            card = d.strip()
            card_idx, value = process_card(card)
            cards[card_idx] = value

    seen = expand_duplicates(cards)
    answer = sum(seen.values())

    assert answer == 30

    print("Tests passed.")


def puzzle():
    cards = {}
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            card = d.strip()
            card_idx, value = process_card(card)
            cards[card_idx] = value

    seen = expand_duplicates(cards)
    answer = sum(seen.values())

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
