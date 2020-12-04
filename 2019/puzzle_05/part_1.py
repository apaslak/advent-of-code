#!/usr/bin/env python3

import pdb
# cursor+3 = index of address in input
# memory[cursor+3] = index of actual address in memory
# memory[memory[cursor+3] = value at address in memory

def determine_inputs(memory, mode, index):
    if mode[0] == '0':
        input1 = memory[memory[index+1]]
    else:
        input1 = memory[index+1]

    try:
        if mode[1] == '0':
            input2 = memory[memory[index+2]]
        else:
            input2 = memory[index+2]
    except:
        input2 = None

    return input1, input2

def debug(whatever):
    return
    print(whatever)

def run(init_memory, user_input):
    output = []
    memory = init_memory.copy()

    next_instruction = 0
    cursor = 0
    halted = False
    while not halted:
        if cursor == next_instruction:
            opcode = int(str(memory[cursor])[-2:])
            modes = str(memory[cursor])[:-2][::-1] + '0000'
            debug(f'opcode: {opcode}')
            if opcode == 1:
                next_instruction += 4
                input1, input2 = determine_inputs(memory, modes, cursor)
                memory[memory[cursor+3]] = input1 + input2
            elif opcode == 2:
                next_instruction += 4
                input1, input2 = determine_inputs(memory, modes, cursor)
                memory[memory[cursor+3]] = input1 * input2
            elif opcode == 3:
                next_instruction += 2
                memory[memory[cursor+1]] = user_input
            elif opcode == 4:
                next_instruction += 2
                test_result, _ = determine_inputs(memory, modes, cursor)
                output.append(test_result)
            elif opcode == 99:
                halted = True
            else:
                raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
        debug(f'cursor: {cursor}, next_instruction: {next_instruction}')
        cursor += 1

    return memory, output

def puzzle5():
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]
    memory, output = run(memory, 1)
    print(f'{output}')

if __name__ == '__main__':
    puzzle5()
