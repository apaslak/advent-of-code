#!/usr/bin/env python3

import pdb
from itertools import permutations

# cursor+3 = index of address in input
# memory[cursor+3] = index of actual address in memory
# memory[memory[cursor+3] = value at address in memory

# phase and then input

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

def intcode(init_memory, user_input, phase=-1):
    output = []
    memory = init_memory.copy()
    inputs = user_input if phase == -1 else [user_input, phase]

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
                selected_input = user_input if phase == -1 else inputs.pop()
                # selected_input = input("Enter input: ")
                memory[memory[cursor+1]] = int(selected_input)
            elif opcode == 4:
                next_instruction += 2
                test_result, _ = determine_inputs(memory, modes, cursor)
                output.append(test_result)
            elif opcode == 5:
                input1, input2 = determine_inputs(memory, modes, cursor)
                if input1 != 0:
                    cursor = input2-1
                    next_instruction = input2
                else:
                    next_instruction += 3
            elif opcode == 6:
                input1, input2 = determine_inputs(memory, modes, cursor)
                if input1 == 0:
                    cursor = input2-1
                    next_instruction = input2
                else:
                    next_instruction += 3
            elif opcode == 7:
                next_instruction += 4
                input1, input2 = determine_inputs(memory, modes, cursor)
                if input1 < input2:
                    value = 1
                else:
                    value = 0
                memory[memory[cursor+3]] = value
            elif opcode == 8:
                next_instruction += 4
                input1, input2 = determine_inputs(memory, modes, cursor)
                if input1 == input2:
                    value = 1
                else:
                    value = 0
                memory[memory[cursor+3]] = value
            elif opcode == 99:
                halted = True
            else:
                raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
        debug(f'cursor: {cursor}, next_instruction: {next_instruction}')
        cursor += 1

    return memory, output[0]

def amp_system(memory, sequence, loop_setting='series'):
    thing = 0
    for phase in sequence:
        print(f'sequence: {sequence}, phase: {phase}')
        _, thing = intcode(memory, thing, int(phase))
    if loop_setting == 'feedback':
        last_thing = -1
        halted = False
        while not halted:
            _, thing = intcode(memory, thing, -1)
            if last_thing == thing:
                halted = True
    return thing

def puzzle7(memory, phase_settings='01234', loop_setting='series'):
    winning_sequence = '00000'
    largest = 0
    for sequence_arr in list(permutations(phase_settings, len(phase_settings))):
        sequence = ''.join(sequence_arr)
        output = amp_system(memory, sequence, loop_setting)
        if output > largest:
            largest = output
            winning_sequence = sequence

    return largest, winning_sequence


if __name__ == '__main__':
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]
    memory, output = intcode(memory, 5)
    print(f'{output}')

    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]
    largest, sequence = puzzle7(memory)
    print(f'7a: {largest}')

    largest, sequence = puzzle7(memory, '56789')
    print(f'7b: {largest}')
