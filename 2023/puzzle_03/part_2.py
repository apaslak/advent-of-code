#!/usr/bin/env python3


def is_dot(c):
    return c == "."


def is_symbol(c):
    return not c.isdigit() and not is_dot(c)


def is_symbol_adjacent(schematic, i, j):
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

        if is_symbol(neighbor):
            return True

    return False


def sum_engine_parts(schematic):
    """
    y = row
    x = column
    """
    sum = 0
    possible_number = ''
    check = True
    for i, y in enumerate(schematic):
        for j, x in enumerate(y):
            is_number = x.isdigit()
            if is_number and check:
                if is_symbol_adjacent(schematic, i, j):
                    check = False

            if is_number:
                possible_number += x

            if not is_number and not check:
                sum += int(possible_number)

            if not is_number:
                possible_number = ''
                check = True

        if is_number and not check:
            sum += int(possible_number)

        possible_number = ''
        check = True
    return sum


def test_examples():
    schematic = []
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            schematic.append(list(d.strip()))

    assert sum_engine_parts(schematic) == 4361
    print("Tests passed.")


def puzzle():
    schematic = []
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            schematic.append(list(d.strip()))

    answer = sum_engine_parts(schematic)
    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
