#!/usr/bin/env python3

from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def calculate_ways_to_win(race):
    ways = 0
    t, d = race
    for time_holding_button in range(t):
        time_left = t - time_holding_button
        distance_traveled = time_holding_button * time_left
        if distance_traveled > d:
            ways += 1

    return ways


def create_races(times, distances):
    return set(zip(times, distances))


def parse_input_file(file_name):
    times = []
    distances = []
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            _, numbers = row.split(":")
            parsed_numbers = [int(i) for i in numbers.split(" ") if i]
            if row.startswith("Time"):
                times = parsed_numbers
            else:
                distances = parsed_numbers

    return times, distances


def test_examples():
    answer = 1
    times, distances = parse_input_file(r"test_input.txt")
    races = create_races(times, distances)

    for race in races:
        answer *= calculate_ways_to_win(race)

    assert answer == 288

    print("Tests passed.")


def puzzle():
    answer = 1
    times, distances = parse_input_file(r"input.txt")
    races = create_races(times, distances)

    for race in races:
        answer *= calculate_ways_to_win(race)

    print(f'{answer}')


if __name__ == '__main__':
    #test_examples()
    puzzle()
