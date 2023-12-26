#!/usr/bin/env python3


def identify_calibration_value(line):
    first_char = None
    for char in line:
        if char.isdigit():
            first_char = char
            break

    second_char = None
    for char in line[::-1]:
        if char.isdigit():
            second_char = char
            break

    if not first_char or not second_char:
        raise Exception("string had no digits")

    return int(f"{first_char}{second_char}")


def test_examples():
    assert identify_calibration_value("1abc2") == 12
    assert identify_calibration_value("pqr3stu8vwx") == 38
    assert identify_calibration_value("a1b2c3d4e5f") == 15
    assert identify_calibration_value("treb7uchet") == 77
    print("Tests passed.")


def puzzle1():
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += identify_calibration_value(d.strip())

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle1()
