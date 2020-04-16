import pdb

def test_examples():
    with open(r'example1_input.txt', 'r') as file:
        memory = [line.strip() for line in file.readlines()]

def puzzle10():
    with open(r'input.txt', 'r') as file:
        memory = [line.strip() for line in file.readlines()]

    print(f'10a: {output}')

if __name__ == '__main__':
    test_examples()
    puzzle10()
