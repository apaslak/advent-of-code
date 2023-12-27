#!/usr/bin/env python3


from collections import defaultdict


def is_asterisk(c):
    return c == "*"


def adjacent_asterisks(schematic, i, j, asterisks_found):
    directions = [
        (-1, 1), (0, 1), (1, 1),
        (-1, 0), (1, 0),
        (-1, -1), (0, -1), (1, -1),
    ]
    for dj, di in directions:
        new_j, new_i = j + dj, i + di
        try:
            neighbor = schematic[new_i][new_j]
        except IndexError:
            continue

        if is_asterisk(neighbor):
            asterisks_found.add((new_i, new_j))

    return asterisks_found


def find_potential_gears(schematic):
    """
    y = row
    x = column
    """
    possible_number = ''
    asterisks_found = set()
    # asterisk_to_parts is a dict where the keys are tuples indicating the location of the asterisk
    # and the values are sets of part numbers
    asterisk_to_parts = defaultdict(set)
    for i, y in enumerate(schematic):
        for j, x in enumerate(y):
            is_number = x.isdigit()
            if is_number:
                asterisks_found.update(adjacent_asterisks(schematic, i, j, asterisks_found))
                possible_number += x

            if not is_number and len(asterisks_found) > 0:
                for asterisk in asterisks_found:
                    asterisk_to_parts[asterisk].add(int(possible_number))

            if not is_number:
                possible_number = ''
                asterisks_found = set()

        if is_number and len(asterisks_found) > 0:
            for asterisk in asterisks_found:
                asterisk_to_parts[asterisk].add(int(possible_number))

        possible_number = ''
        asterisks_found = set()
    return asterisk_to_parts


def sum_gear_ratios(schematic):
    sum = 0
    asterisk_to_parts = find_potential_gears(schematic)
    for asterisk, part_numbers in asterisk_to_parts.items():
        if len(part_numbers) == 2:
            sum += part_numbers.pop() * part_numbers.pop()

    return sum


def test_examples():
    schematic = []
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            schematic.append(list(d.strip()))

    assert sum_gear_ratios(schematic) == 467835
    print("Tests passed.")


def puzzle():
    schematic = []
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            schematic.append(list(d.strip()))

    answer = sum_gear_ratios(schematic)
    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
