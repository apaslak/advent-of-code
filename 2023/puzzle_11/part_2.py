#!/usr/bin/env python3

from itertools import combinations
from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def rotate_map_clockwise(map):
    new_map = []
    num_rows, num_cols = len(map), len(map[0])
    for i in range(num_cols):
        j = num_rows-1
        col = []
        while j >= 0:
            col.append(map[j][i])
            j -= 1
        new_map.append(col)
    return new_map


def identify_expansions(map):
    row_expansions = []
    for i, row in enumerate(map):
        if len(set(row)) == 1:
            row_expansions.append(i)

    map = rotate_map_clockwise(map)

    col_expansions = []
    for i, row in enumerate(map):
        if len(set(row)) == 1:
            col_expansions.append(i)

    return row_expansions, col_expansions


def find_and_label_galaxies(map):
    num_galaxies = 0
    galaxies = {}
    for i, row in enumerate(map):
        galaxy_indices = [idx for idx, v in enumerate(row) if v == "#"]
        for galaxy in galaxy_indices:
            galaxy_label = str(num_galaxies + 1)
            row[galaxy] = galaxy_label
            galaxies[galaxy_label] = (i, galaxy)
            num_galaxies += 1
    return galaxies


def find_pairs(galaxies):
    return list(combinations(galaxies.keys(), r=2))


def update_coord_after_expansion(expansions, coord, expansion_size):
    new_coord = coord
    for e in expansions:
        if e < coord:
            new_coord = new_coord + expansion_size-1

    return new_coord


def find_shortest_path(galaxies, a, b, row_expansions, col_expansions, expansion_size):
    a_row, a_col = galaxies[a]
    b_row, b_col = galaxies[b]

    a_row = update_coord_after_expansion(row_expansions, a_row, expansion_size)
    a_col = update_coord_after_expansion(col_expansions, a_col, expansion_size)

    b_row = update_coord_after_expansion(row_expansions, b_row, expansion_size)
    b_col = update_coord_after_expansion(col_expansions, b_col, expansion_size)

    return abs(a_row - b_row) + abs(a_col - b_col)


def sum_shortest_paths(map, galaxies, row_expansions, col_expansions, expansion_size):
    answer = 0
    pairs = find_pairs(galaxies)
    for a, b in pairs:
        answer += find_shortest_path(galaxies, a, b, row_expansions, col_expansions, expansion_size)

    return answer


def parse_input_file(file_name):
    map = []
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            map.append(list(row))

    return map


def test_examples():
    map = parse_input_file(r"test_input.txt")
    row_expansions, col_expansions = identify_expansions(map)
    galaxies = find_and_label_galaxies(map)
    expansion_size = 2
    answer = sum_shortest_paths(map, galaxies, row_expansions, col_expansions, expansion_size)

    assert answer == 374

    expansion_size = 10
    answer = sum_shortest_paths(map, galaxies, row_expansions, col_expansions, expansion_size)

    assert answer == 1030

    expansion_size = 100
    answer = sum_shortest_paths(map, galaxies, row_expansions, col_expansions, expansion_size)

    assert answer == 8410

    print("Tests passed.")


def puzzle():
    map = parse_input_file(r"input.txt")
    row_expansions, col_expansions = identify_expansions(map)
    galaxies = find_and_label_galaxies(map)
    expansion_size = 1_000_000

    answer = sum_shortest_paths(map, galaxies, row_expansions, col_expansions, expansion_size)

    print(f'{answer}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
