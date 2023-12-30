#!/usr/bin/env python3

from collections import deque
from sys import argv

"""
         (0,  1)
(-1,  0) (0,  0) (1,  0)
         (0, -1)
rotated clockwise...
         (-1, 0)
(0,  -1) ( 0, 0) (0,  1)
         ( 1, 0)
"""

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

MAP_LEGEND = {
    "|": set([NORTH, SOUTH]),
    "-": set([EAST, WEST]),
    "L": set([NORTH, EAST]),
    "J": set([NORTH, WEST]),
    "7": set([SOUTH, WEST]),
    "F": set([SOUTH, EAST]),
    ".": set([]),
}
DELTAS = [WEST, NORTH, EAST, SOUTH]


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def map_size(map):
    return len(map), len(map[0])


def print_map(map):
    [print(i) for i in map]


def identity_s_pipe_shape(map, x, y):
    connected_directions = set()
    directions = [
        (NORTH, SOUTH),
        (EAST, WEST),
        (SOUTH, NORTH),
        (WEST, EAST),
    ]
    for to_direction, from_direction in directions:
        try:
            dx, dy = to_direction
            neighbor_shape, _ = map[x + dx][y + dy]
            if from_direction in MAP_LEGEND[neighbor_shape]:
                connected_directions.add(to_direction)
            if len(connected_directions) == 2:
                break
        except IndexError:
            pass

    for pipe, directions in MAP_LEGEND.items():
        if directions == connected_directions:
            return pipe

    raise Exception("Couldn't identify S shape")


def is_valid_move(map, current_position, next_position):
    current_x, current_y = current_position
    current_pipe, _ = map[current_x][current_y]

    next_x, next_y = next_position
    next_pipe, _ = map[next_x][next_y]

    if next_pipe == "S":
        return False

    if current_pipe == "S":
        s_shape = identity_s_pipe_shape(map, current_x, current_y)
        valid_deltas = MAP_LEGEND.get(s_shape)
    else:
        valid_deltas = MAP_LEGEND.get(current_pipe)

    valid_moves = set([(current_x + xd, current_y + yd) for xd, yd in valid_deltas])
    if next_position in valid_moves:
        return True

    return False


def get_possible_moves(map, x, y):
    num_rows, num_cols = map_size(map)
    valid_moves = []

    for x_delta, y_delta in DELTAS:
        new_x, new_y = x + x_delta, y + y_delta
        if 0 <= new_x < num_rows and 0 <= new_y < num_cols:
            if is_valid_move(map, (x, y), (new_x, new_y)):
                valid_moves.append((new_x, new_y))
    return valid_moves


def locate_starting_point(map):
    queue = deque()

    for i, row in enumerate(map):
        for j, col in enumerate(row):
            shape, _ = col
            if shape == "S":
                queue.append((i, j))
                break
    return queue


def find_farthest_point(map):
    queue = locate_starting_point(map)
    steps = 0
    visited = set()

    while queue:
        x, y = queue.popleft()
        visited.add((x, y))
        _, current_steps = map[x][y]
        steps_to_next_move = current_steps + 1
        possible_moves = get_possible_moves(map, x, y)
        for new_x, new_y in possible_moves:
            if (new_x, new_y) in visited:
                continue
            next_move_shape, _ = map[new_x][new_y]
            map[new_x][new_y] = (next_move_shape, steps_to_next_move)
            if steps_to_next_move > steps:
                steps = steps_to_next_move
            queue.append((new_x, new_y))

    return steps


def count_enclosed_tiles(map):
    enclosed_count = 0
    enclosed = False
    inside_horizontal_line = False
    for i, row in enumerate(map):
        log(f"=== row {i+1} ===")
        for j, col in enumerate(row):
            shape, steps = col
            if steps == 0:
                shape = "."
            if shape == "S":
                shape = identity_s_pipe_shape(map, i, j)
            log(f"shape: {shape}, enclosed: {enclosed}, inside_horizontal_line: {inside_horizontal_line}")
            if shape in ["|", "J", "L"]:
                enclosed = not enclosed
            if shape in ["L", "F"]:
                inside_horizontal_line = True
            if shape in ["7", "J"]:
                inside_horizontal_line = False
            if enclosed and not inside_horizontal_line and steps == 0:
                enclosed_count += 1
                log(f"enclosed_count: {enclosed_count}")
    return enclosed_count


def parse_input_file(file_name):
    map = []
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            map.append([(shape, 0) for shape in list(row)])

    return map


def test_examples():
    map = parse_input_file(r"test_input3.txt")
    find_farthest_point(map)
    answer = count_enclosed_tiles(map)

    assert answer == 4

    map = parse_input_file(r"test_input4.txt")
    find_farthest_point(map)
    answer = count_enclosed_tiles(map)

    assert answer == 8

    map = parse_input_file(r"test_input5.txt")
    find_farthest_point(map)
    answer = count_enclosed_tiles(map)

    assert answer == 10

    print("Tests passed.")


def puzzle():
    map = parse_input_file(r"input.txt")
    find_farthest_point(map)
    answer = count_enclosed_tiles(map)

    print(f'{answer}')


if __name__ == '__main__':
    # test_examples()
    puzzle()
