#!/usr/bin/env python3

from itertools import cycle
from math import lcm
from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def walk(instructions, manual, location):
    steps = 0
    while not location.endswith("Z"):
        next_move = 0 if next(instructions) == "L" else 1

        location = manual[location][next_move]
        steps += 1
    return steps


def parse_input_file(file_name):
    instructions = None
    manual = {}
    starting_nodes = []
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            if not instructions:
                instructions = cycle(list(row))
                continue

            if not row:
                continue

            key, values = row.split(" = ")
            values = values.replace("(", "").replace(")", "").split(", ")
            manual[key] = values
            if key.endswith("A"):
                starting_nodes.append(key)
    return instructions, manual, starting_nodes


def test_examples():
    instructions, manual, starting_nodes = parse_input_file(r"test_input3.txt")

    lcms = [walk(instructions, manual, starting_node) for starting_node in starting_nodes]
    answer = lcm(*lcms)
    assert answer == 6

    print("Tests passed.")


def puzzle():
    instructions, manual, starting_nodes = parse_input_file(r"input.txt")

    lcms = [walk(instructions, manual, starting_node) for starting_node in starting_nodes]
    answer = lcm(*lcms)

    print(f'{answer}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
