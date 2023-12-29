#!/usr/bin/env python3

from sys import argv


def log(s):
    try:
        debug_flag = argv[1]
        if debug_flag:
            print(s)
    except IndexError:
        pass


def find_next_seq(sequence):
    new_seq = []
    for i in range(len(sequence)-1):
        left, right = sequence[i], sequence[i+1]
        new_seq.append(right - left)
    return new_seq


def find_next_value(sequence):
    bottom = len(set(sequence)) == 1
    new_seq = sequence
    stack = [sequence]

    while not bottom:
        new_seq = find_next_seq(new_seq)
        bottom = len(set(new_seq)) == 1
        if not bottom:
            stack.append(new_seq)

    next_value = new_seq[0]

    while stack:
        bottom = stack.pop()
        next_value = bottom[0] - next_value

    return next_value


def do_work(file_name):
    sequences = []
    answer = 0
    with open(file_name, 'r', encoding="utf-8") as input_file:
        data = input_file.readlines()

        for d in data:
            row = d.strip()
            sequence = [int(i) for i in row.split(" ")]
            previous_value = find_next_value(sequence)
            answer += previous_value
            sequences.append([previous_value] + sequence)

    return sequences, answer


def test_examples():
    sequences, answer = do_work(r"test_input.txt")

    assert answer == 2

    print("Tests passed.")


def puzzle():
    sequences, answer = do_work(r"input.txt")

    print(f'{answer}')


if __name__ == '__main__':
    test_examples()
    puzzle()
