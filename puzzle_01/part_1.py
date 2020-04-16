#!/usr/bin/env python3

import pdb
from math import floor

def calculate_fuel(mass):
    return floor(mass / 3) - 2

def test_examples():
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583

def puzzle1():
    fuel_required = 0
    with open(r'input.txt', 'r') as modules_file:
        modules = modules_file.readlines()

        for module in modules:
            fuel_required += calculate_fuel(int(module.strip()))

    print(f'{fuel_required}')

if __name__ == '__main__':
    test_examples()
    puzzle1()
