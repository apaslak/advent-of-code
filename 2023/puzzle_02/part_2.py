#!/usr/bin/env python3

import re


def identify_cube_numbers(color, round):
    regex = r"(?P<color>\d*) " + re.escape(color)
    match = re.search(regex, round)
    try:
        return int(match.group("color"))
    except (AttributeError, IndexError):
        return 0


def identify_minimum_cubes_by_color(game):
    _, rounds = game.split(":")
    rounds = rounds.split(";")
    min_red = 0
    min_green = 0
    min_blue = 0

    for round in rounds:
        red = identify_cube_numbers('red', round)
        green = identify_cube_numbers('green', round)
        blue = identify_cube_numbers('blue', round)

        min_red = max(red, min_red)
        min_green = max(green, min_green)
        min_blue = max(blue, min_blue)

    return min_red, min_green, min_blue


def calculate_power_of_game(game):
    red, green, blue = identify_minimum_cubes_by_color(game)
    return red * green * blue


def test_examples():
    games = [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", {'red': 4, 'green': 2, 'blue': 6}),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", {'red': 1, 'green': 3, 'blue': 4}),
        ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", {'red': 20, 'green': 13, 'blue': 6}),
        ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", {'red': 14, 'green': 3, 'blue': 15}),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", {'red': 6, 'green': 3, 'blue': 2}),
    ]
    for game, minimum_cubes in games:
        expected_power = minimum_cubes['red'] * minimum_cubes['green'] * minimum_cubes['blue']
        actual_power = calculate_power_of_game(game)

        assert actual_power == expected_power

    print("Tests passed.")


def puzzle():
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += calculate_power_of_game(d.strip())

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
