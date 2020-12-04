#!/usr/bin/env python3
from math import ceil

# [
#   [0, 0, 0, 0],
#   [0, 0, 0, 0]
# ]
# charted_map[row][column]
# charted_map[y][x]

def print_map(charted_map):
    for row in charted_map:
        print(''.join(row))

def update_point(charted_map, pointer_y, pointer_x, indicator):
    if charted_map[pointer_y][pointer_x] == '.':
        charted_map[pointer_y][pointer_x] = indicator
    elif charted_map[pointer_y][pointer_x] == 'o':
        raise ValueError("Uh. something is wrong here.")
    else:
        charted_map[pointer_y][pointer_x] = 'x'
    return charted_map

def select_indicator(default_indicator, is_edge):
    if is_edge:
        return '+'
    else:
        return default_indicator

def plot_line(charted_map, line, pointer_x, pointer_y):
    points = []
    for point in line:
        direction = point[0]
        hops = int(point[1:])
        if direction == 'R':
            for i in range(1, hops+1):
                indicator = select_indicator('-', i == hops)
                charted_map = update_point(charted_map, pointer_y, pointer_x+i, indicator)
                points.append((pointer_y, pointer_x+i))
            pointer_x = pointer_x + hops
        elif direction == 'L':
            for i in range(1, hops+1):
                indicator = select_indicator('-', i == hops)
                charted_map = update_point(charted_map, pointer_y, pointer_x-i, indicator)
                points.append((pointer_y, pointer_x-i))
            pointer_x = pointer_x - hops
        elif direction == 'U':
            for i in range(1, hops+1):
                indicator = select_indicator('|', i == hops)
                charted_map = update_point(charted_map, pointer_y-i, pointer_x, indicator)
                points.append((pointer_y-i, pointer_x))
            pointer_y = pointer_y - hops
        elif direction == 'D':
            for i in range(1, hops+1):
                indicator = select_indicator('|', i == hops)
                charted_map = update_point(charted_map, pointer_y+i, pointer_x, indicator)
                points.append((pointer_y+i, pointer_x))
            pointer_y = pointer_y + hops
        else:
            raise ValueError("What direction is that")

    return points

def calculate_manhattan_distance(central_port_x, central_port_y, intersection_points):
    least = 500000
    for y, x in intersection_points:
        distance = abs(central_port_x - x) + abs(central_port_y - y)
        if distance < least:
            least = distance

    return least

def create_empty_map(n):
    rows, cols = (n, n)
    central_port_x = 0
    central_port_y = int(ceil(n/2)) - 1
    charted_map = [['.' for i in range(cols)] for j in range(rows)]
    charted_map[central_port_y][central_port_x] = 'o'

    return charted_map

def intersection(lst2, lst1):
    return set(lst2).intersection(lst1)

def _calculate_central_port_y(n):
    return int(ceil(n/2)) - 1

def test_examples():
    n = 25
    line1 = 'R8,U5,L5,D3'.split(',')
    line2 = 'U7,R6,D4,L4'.split(',')
    charted_map = create_empty_map(n)
    central_port_x = 0
    central_port_y = _calculate_central_port_y(n)
    line1_points = plot_line(charted_map,
                             line1,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    line2_points = plot_line(charted_map,
                             line2,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    intersection_points = intersection(line1_points, line2_points)
    assert calculate_manhattan_distance(central_port_x, central_port_y, intersection_points) == 6

    n = 239
    line1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    line2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    charted_map = create_empty_map(n)
    central_port_x = 0
    central_port_y = _calculate_central_port_y(n)
    line1_points = plot_line(charted_map,
                             line1,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    line2_points = plot_line(charted_map,
                             line2,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    intersection_points = intersection(line1_points, line2_points)
    assert calculate_manhattan_distance(central_port_x, central_port_y, intersection_points) == 159

    n = 239
    line1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    line2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')
    charted_map = create_empty_map(n)
    central_port_x = 0
    central_port_y = _calculate_central_port_y(n)
    line1_points = plot_line(charted_map,
                             line1,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    line2_points = plot_line(charted_map,
                             line2,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    intersection_points = intersection(line1_points, line2_points)
    assert calculate_manhattan_distance(central_port_x, central_port_y, intersection_points) == 135

def puzzle3():
    n = 20000
    with open(r'input.txt', 'r') as file:
        map_file = file.readlines()
        line1 = map_file[0].strip().split(',')
        line2 = map_file[1].strip().split(',')

    charted_map = create_empty_map(n)
    central_port_x = 0
    central_port_y = int(ceil(n/2)) - 1
    line1_points = plot_line(charted_map,
                             line1,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    line2_points = plot_line(charted_map,
                             line2,
                             pointer_x=central_port_x,
                             pointer_y=central_port_y)
    intersection_points = intersection(line1_points, line2_points)
    result = calculate_manhattan_distance(central_port_x, central_port_y, intersection_points)
    print(f'{result}')

if __name__ == '__main__':
    test_examples()
    puzzle3()
