#!/usr/bin/env python3

import re


def identify_cube_numbers(color, round):
    regex = r"(?P<color>\d*) " + re.escape(color)
    match = re.search(regex, round)
    try:
        return int(match.group("color"))
    except (AttributeError, IndexError):
        return 0


def possible(game_data, game):
    _, rounds = game.split(":")
    rounds = rounds.split(";")
    for round in rounds:
        red = identify_cube_numbers('red', round)
        green = identify_cube_numbers('green', round)
        blue = identify_cube_numbers('blue', round)

        if red > game_data['red']:
            return False

        if green > game_data['green']:
            return False

        if blue > game_data['blue']:
            return False

    return True


def find_possible_game_id(game_data, game):
    if possible(game_data, game):
        regex = re.match("^Game (?P<id>\d{1,3})", game)
        game_id = regex.group("id")
        return int(game_id)
    return 0


def test_examples():
    game_data = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    games = [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
        ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
        ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
    ]
    sum = 0
    for game, possibility in games:
        game_id = find_possible_game_id(game_data, game)
        sum += game_id
        assert (game_id > 0) == possibility

    assert sum == 8

    print("Tests passed.")


def puzzle():
    game_data = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += find_possible_game_id(game_data, d.strip())

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
