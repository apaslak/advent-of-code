#!/usr/bin/env python3

import re
from sys import argv

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def extract_digit(possible_number, direction):
    for word, digit in DIGITS.items():
        search_word = word[::-1] if direction == 'backward' else word
        if search_word in possible_number:
            return DIGITS[word]


def find_digit(line, direction='forward'):
    if direction == 'backward':
        line = line[::-1]

    i = 0
    while i + 5 < len(line):
        if line[i].isdigit():
            log(f"found digit: {line[i]}")
            return line[i]

        if line[i+1].isdigit():
            log(f"found digit: {line[i+1]}")
            return line[i+1]

        possible_number = line[i:i+5]
        log(f"possible_number: {possible_number}")
        found_digit = extract_digit(possible_number, direction)
        if found_digit:
            log(f"extracted digit: {found_digit}")
            return found_digit
        i += 1

    while i < len(line):
        if line[i].isdigit():
            log(f"found digit: {line[i]}")
            return line[i]

        if line[i+1].isdigit():
            log(f"found digit: {line[i+1]}")
            return line[i+1]

        possible_number = line[i:]
        log(f"possible_number: {possible_number}")
        found_digit = extract_digit(possible_number, direction)
        if found_digit:
            log(f"extracted digit: {found_digit}")
            return found_digit
        i += 1

    import pdb; pdb.set_trace()
    raise Exception("could not find number")


def identify_calibration_value(line):
    log(f"line: {line}")
    first_digit = find_digit(line, direction='forward')
    second_digit = find_digit(line, direction='backward')

    if not first_digit or not second_digit:
        raise Exception("string had no digits")

    value = int(f"{first_digit}{second_digit}")
    log(f"value: {value}")
    return value


def test_examples():
    assert identify_calibration_value("two1nine") == 29, "two1nine"
    assert identify_calibration_value("eightwothree") == 83, "eightwothree"
    assert identify_calibration_value("abcone2threexyz") == 13, "abcone2threexyz"
    assert identify_calibration_value("xtwone3four") == 24, "xtwone3four"
    assert identify_calibration_value("4nineeightseven2") == 42, "4nineeightseven2"
    assert identify_calibration_value("zoneight234") == 14, "zoneight234"
    assert identify_calibration_value("7pqrstsixteen") == 76, "7pqrstsixteen"
    assert identify_calibration_value("eightfivetwone") == 81, "eightfivetwone"
    assert identify_calibration_value("eighthree") == 83, "eighthree"
    assert identify_calibration_value("f1six") == 16, "f1six"
    log("Tests passed.")


def puzzle1():
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            line = identify_calibration_value(d.strip())
            log(f"{d.strip()}: {line}")
            answer += line

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle1()
