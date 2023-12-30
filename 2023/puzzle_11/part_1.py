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


def print_map(map, join=False):
    if join:
        for row in map:
            print(''.join(row))
    else:
        [print(i) for i in map]


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


def rotate_map_counter_clockwise(map):
    new_map = [[] for i in range(len(map[0]))]
    for row in map:
        i = 0
        for j in range(len(row)-1, -1, -1):
            new_map[i].append(row[j])
            i += 1

    return new_map


def expand_map(map):
    new_map = []
    for row in map:
        new_map.append(row)
        if len(set(row)) == 1:
            new_map.append(row)

    map = rotate_map_clockwise(new_map)

    new_map = []
    for row in map:
        new_map.append(row)
        if len(set(row)) == 1:
            new_map.append(row)

    map = rotate_map_counter_clockwise(new_map)

    return map


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


def find_shortest_path(galaxies, a, b):
    a_coords, b_coords = galaxies[a], galaxies[b]
    return abs(a_coords[0] - b_coords[0]) + abs(a_coords[1] - b_coords[1])


def sum_shortest_paths(map, galaxies):
    answer = 0
    pairs = find_pairs(galaxies)
    for a, b in pairs:
        answer += find_shortest_path(galaxies, a, b)

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
    map = expand_map(map)
    galaxies = find_and_label_galaxies(map)
    answer = sum_shortest_paths(map, galaxies)

    assert answer == 374

    print("Tests passed.")


def puzzle():
    map = parse_input_file(r"input.txt")
    map = expand_map(map)
    galaxies = find_and_label_galaxies(map)
    answer = sum_shortest_paths(map, galaxies)

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
