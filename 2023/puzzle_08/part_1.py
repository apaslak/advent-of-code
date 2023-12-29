#!/usr/bin/env python3

from itertools import cycle
from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def walk(instructions, manual):
    location = "AAA"
    steps = 0
    while location != "ZZZ":
        next_move = 0 if next(instructions) == "L" else 1
        location = manual[location][next_move]
        steps += 1
    return steps


def parse_input_file(file_name):
    instructions = None
    manual = {}
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
    return instructions, manual


def test_examples():
    instructions, manual = parse_input_file(r"test_input1.txt")

    steps = walk(instructions, manual)
    assert steps == 2

    instructions, manual = parse_input_file(r"test_input2.txt")

    steps = walk(instructions, manual)
    assert steps == 6

    print("Tests passed.")


def puzzle():
    instructions, manual = parse_input_file(r"input.txt")

    steps = walk(instructions, manual)

    print(f'{steps}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
