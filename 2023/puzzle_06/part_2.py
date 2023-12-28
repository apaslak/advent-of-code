#!/usr/bin/env python3

from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def calculate_ways_to_win(t, d):
    ways = 0
    for time_holding_button in range(t):
        time_left = t - time_holding_button
        distance_traveled = time_holding_button * time_left
        if distance_traveled > d:
            ways += 1

    return ways


def parse_input_file(file_name):
    time = None
    distance = None
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            _, numbers = row.split(":")
            number = int(numbers.replace(" ", ""))
            if row.startswith("Time"):
                time = number
            else:
                distance = number

    return time, distance


def test_examples():
    time, distance = parse_input_file(r"test_input.txt")
    answer = calculate_ways_to_win(time, distance)

    assert answer == 71503

    print("Tests passed.")


def puzzle():
    time, distance = parse_input_file(r"input.txt")
    answer = calculate_ways_to_win(time, distance)

    print(f'{answer}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
