#!/usr/bin/env python3

from sys import argv


class RangeDict(dict):
    def __getitem__(self, key):
        for rnge, start_dest in self.items():
            if key in rnge:
                beginning_of_range = rnge[0]
                diff = key - beginning_of_range
                return start_dest + diff
        return key


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def create_mapping(m, line):
    dest, src, rnge = list(map(lambda x: int(x), line.split(" ")))
    m[range(src, src+rnge)] = dest
    return m


def extract_seed_list(line):
    _, seeds = line.split(":")
    return list(map(lambda x: int(x), seeds.strip().split(" ")))


def update_almanac(almanac, line):
    if not line:
        return almanac

    elif line.startswith("seed-to-soil"):
        almanac["wip"] = RangeDict()
    elif line.startswith("soil-to-fertilizer"):
        almanac["seed-to-soil"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    elif line.startswith("fertilizer-to-water"):
        almanac["soil-to-fertilizer"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    elif line.startswith("water-to-light"):
        almanac["fertilizer-to-water"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    elif line.startswith("light-to-temperature"):
        almanac["water-to-light"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    elif line.startswith("temperature-to-humidity"):
        almanac["light-to-temperature"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    elif line.startswith("humidity-to-location"):
        almanac["temperature-to-humidity"] = almanac["wip"]
        almanac["wip"] = RangeDict()
    else:
        almanac["wip"] = create_mapping(almanac["wip"], line)

    almanac["humidity-to-location"] = almanac["wip"]

    return almanac


def find_lowest_seed_location(seeds, almanac):
    lowest_location = float('inf')
    for seed in seeds:
        value = seed
        mappings = [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]
        for i in mappings:
            log(f"{i}: {value}")
            value = almanac[i][value]

        if value < lowest_location:
            lowest_location = value

    return lowest_location


def test_examples():
    seeds = None
    almanac = {}
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            line = d.strip()

            if line.startswith("seeds"):
                seeds = extract_seed_list(line)
            else:
                almanac = update_almanac(almanac, line)

    answer = find_lowest_seed_location(seeds, almanac)
    assert answer == 35

    print("Tests passed.")


def puzzle():
    seeds = None
    almanac = {}
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            line = d.strip()

            if line.startswith("seeds"):
                seeds = extract_seed_list(line)
            else:
                almanac = update_almanac(almanac, line)

    answer = find_lowest_seed_location(seeds, almanac)

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
