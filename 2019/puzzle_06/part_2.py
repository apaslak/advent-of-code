#!/usr/bin/env python3

import pdb

class Planet:
    def __init__(self, name, orbits_planet=None, orbited_by=None):
        self.name = name
        self.orbits_planet = orbits_planet
        self.orbited_by = [] if orbited_by is None else orbited_by

    def add_orbit(self, planet):
        self.orbits_planet = planet

    def add_orbited_by(self, planet):
        self.orbited_by.append(planet)

    def calculate_orbital_length(self, total=0):
        if self.orbits_planet is None:
            return total
        return self.orbits_planet.calculate_orbital_length(total+1)

    def calculate_orbital_path(self, path=None):
        if path is None:
            path = []
        if self.orbits_planet is None:
            return path
        return self.orbits_planet.calculate_orbital_path(path + [self.orbits_planet])

    def calculate_least_orbital_transfers_to(self, them, last_known):
        their_path = them.calculate_orbital_path()[::-1]
        my_path = self.calculate_orbital_path()[::-1]
        last_step = 0
        for i, (theirs, mine) in enumerate(zip(their_path, my_path)):
            if theirs.name != mine.name:
                last_step = i-1
                break
            else:
                last_known = mine

        result = len(my_path)-last_step+len(their_path)-last_step
        return result-2


    def __repr__(self):
        return f'Planet(name={self.name})'


def init_db(orbits):
    db = {}
    for orbit in orbits:
        center, orbiter = orbit.split(')')
        if center not in db:
            db[center] = Planet(name=center)
        if orbiter not in db:
            db[orbiter] = Planet(name=orbiter)
        db[orbiter].add_orbit(db[center])
        db[center].add_orbited_by(db[orbiter])
    return db

def puzzle6():
    with open(r'input.txt', 'r') as file:
        orbits = [orbit.strip() for orbit in file.readlines()]

    db = init_db(orbits)

    result = 0
    for planet in db:
        result += db[planet].calculate_orbital_length()

    print(f'calculate_orbital_length: {result}')
    result = db['SAN'].calculate_least_orbital_transfers_to(db['YOU'], db['COM'])
    print(f'calculate_least_orbital_transfers_to(santa): {result}')

def test_examples():
    orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
    db = init_db(orbits)
    result = 0
    for planet in db:
        result += db[planet].calculate_orbital_length()

    assert result == 42

    orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L',
              'K)YOU', 'I)SAN']
    db = init_db(orbits)

    result = db['SAN'].calculate_least_orbital_transfers_to(db['YOU'], db['COM'])

    assert result == 4

if __name__ == '__main__':
    test_examples()
    puzzle6()
