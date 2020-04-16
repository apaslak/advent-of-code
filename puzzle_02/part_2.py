#!/usr/bin/env python3

def intcode(init_memory, noun=None, verb=None):
    memory = init_memory.copy()
    if noun:
        memory[1] = noun
    if verb:
        memory[2] = verb

    for instruction in range(0, len(memory)-1):
        if instruction % 4 == 0:
            opcode = memory[instruction]
            if opcode == 1:
                memory[memory[instruction+3]] = memory[memory[instruction+1]] + memory[memory[instruction+2]]
            elif opcode == 2:
                memory[memory[instruction+3]] = memory[memory[instruction+1]] * memory[memory[instruction+2]]
            elif opcode == 99:
                pass
            else:
                raise ValueError(f'{opcode}')

    return memory

def test_examples():
    assert intcode([1,0,0,0,99]) == [2,0,0,0,99]
    assert intcode([2,3,0,3,99]) == [2,3,0,6,99]
    assert intcode([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert intcode([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def puzzle2():
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]

    for noun in range(0, 99):
        for verb in range(0, 99):
            result = intcode(memory, noun, verb)
            if result[0] == 19690720:
                print(f'noun: {noun}, verb: {verb}')
                answer = 100 * noun + verb
                print(f'{answer}')

if __name__ == '__main__':
    test_examples()
    puzzle2()
