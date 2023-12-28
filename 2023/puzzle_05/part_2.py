#!/usr/bin/env python3

import math
from sys import argv


class RangeDict(dict):
    def __getitem__(self, key):
        for rnge, start_dest in self.items():
            if key in rnge:
                # log(f"Found {key} in {rnge}")
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


def sqrt(i):
    step = int(math.sqrt(i))
    return step


def create_mapping(m, line):
    dest, src, rnge = list(map(lambda x: int(x), line.split(" ")))
    m[range(src, src+rnge)] = dest
    return m


def extract_seed_list(seeds, line):
    _, seeds_str = line.split(":")
    seed_list = list(map(lambda x: int(x), seeds_str.strip().split(" ")))

    for i in range(0, len(seed_list), 2):
        beginning_range = seed_list[i]
        end_range = beginning_range + seed_list[i+1]
        rnge = [beginning_range, end_range]
        seeds.append(rnge)

    return seeds


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


def translate_seed_to_location(almanac, seed):
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
        value = almanac[i][value]

    return value


def find_lowest_in_range(almanac, left, right, step):
    lowest_location = float('inf')
    current_seed = None
    for seed in range(left, right, step):
        value = translate_seed_to_location(almanac, seed)

        if value < lowest_location:
            # log(f"    () Set lowest_location to {value:_}")
            lowest_location = value
            current_seed = seed

    return lowest_location, current_seed


def find_lowest_seed_location(seeds, almanac):
    lowest = {}
    for seed_range in seeds:
        log("======================================")
        log(f"Processing seed range: [{seed_range[0]:_}, {seed_range[1]:_}]")
        current_seed = None
        lowest_location = float('inf')
        left, right = seed_range
        step = sqrt(right - left)

        while step > 0:
            log(f"range is: {left:_}, {right:_}, range length is: {(right - left):_}, step is {step:_}")
            location, new_seed = find_lowest_in_range(almanac, left, right, step)
            log(f"found location {location:_}, new_seed {new_seed:_}")

            if location < lowest_location:
                log(f"+ Set lowest_location to {location:_}")
                lowest_location = location
                current_seed = new_seed

                range_length = right - left
                padding = int(range_length/2)
                left, right = max(left, current_seed - padding), current_seed
                step = sqrt(right - left)
            else:
                log("- found location was bigger than lowest_location")
                range_length = right - left
                padding = int(range_length/2)
                left, right = max(left, current_seed - padding), right
                step = sqrt(right - left)

            log("---")

        lowest[lowest_location] = current_seed
        log(f"=> appended location {lowest_location:_}")

    answer = sorted(lowest.keys())[0]
    return answer, lowest[answer]


def test_examples():
    seeds = []
    almanac = {}
    with open(r'test_input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            line = d.strip()

            if line.startswith("seeds"):
                seeds = extract_seed_list(seeds, line)
            else:
                almanac = update_almanac(almanac, line)

    answer, _ = find_lowest_seed_location(seeds, almanac)
    assert answer == 46

    print("Tests passed.")


def puzzle():
    seeds = []
    almanac = {}
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            line = d.strip()

            if line.startswith("seeds"):
                seeds = extract_seed_list(seeds, line)
            else:
                almanac = update_almanac(almanac, line)

    answer, seed = find_lowest_seed_location(seeds, almanac)

    # established wrong answers, so i don't keep trying them
    wrong_answers = [
        41222969,
        41222970,
        41227364,
        41238736,
    ]
    assert answer not in wrong_answers, "found incorrect answer again :("

    print(f'{answer} | {answer:_}')


if __name__ == '__main__':
    test_examples()
    puzzle()
