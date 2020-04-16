#!/usr/bin/env python3

import pdb
from math import floor

def calculate_fuel(mass, additional_fuel=0):
    calculated_fuel = floor(mass / 3) - 2
    if calculated_fuel <= 0:
        return additional_fuel
    return calculate_fuel(calculated_fuel, calculated_fuel+additional_fuel)

def test_examples():
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 966
    assert calculate_fuel(100756) == 50346

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
