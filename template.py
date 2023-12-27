#!/usr/bin/env python3


def method(param):
    pass


def test_examples():
    assert method(12) == 2
    assert method(14) == 2
    assert method(1969) == 654
    assert method(100756) == 33583
    print("Tests passed.")


def puzzle():
    answer = 0
    with open(r'input.txt', 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            answer += method(d.strip())

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    # puzzle()
