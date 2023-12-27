#!/usr/bin/env python3

from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def calculate_points(num_matches):
    if num_matches == 0:
        return 0
    sum = 1
    for i in range(num_matches-1):
        sum = sum*2
    return sum


def extract_numbers_from_card(card):
    _, numbers = card.split(":")
    winning_numbers, your_numbers = numbers.split("|")
    winning_numbers = set(filter(None, winning_numbers.strip().split(" ")))
    your_numbers = set(filter(None, your_numbers.strip().split(" ")))

    return winning_numbers, your_numbers


def identify_card_value(card):
    winning_numbers, your_numbers = extract_numbers_from_card(card)
    matched_numbers = len(your_numbers) - len(your_numbers - winning_numbers)
    log(f"matched_numbers: {matched_numbers}")
    points = calculate_points(matched_numbers)
    log(f"points: {points}")
    return points


def test_examples():
    answer = 0
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += identify_card_value(d.strip())

    assert answer == 13

    print("Tests passed.")


def puzzle():
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += identify_card_value(d.strip())

    print(f'{answer}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
