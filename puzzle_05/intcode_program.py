#!/usr/bin/env python3

import pdb

class Intcode:
    def __init__(self, memory):
        self.memory = memory

    def run(self):
        output = []
        memory = self.memory

        next_instruction = 0
        cursor = 0
        halted = False
        while not halted:
            if cursor == next_instruction:
                opcode = self.get_opcode(cursor)
                modes = self.get_modes(cursor)
                if opcode == 1:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    memory[memory[cursor+3]] = input1 + input2
                elif opcode == 2:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    memory[memory[cursor+3]] = input1 * input2
                elif opcode == 3:
                    next_instruction += 2
                    selected_input = input("Enter input: ")
                    memory[memory[cursor+1]] = int(selected_input)
                elif opcode == 4:
                    next_instruction += 2
                    test_result, _ = self.determine_inputs(memory, modes, cursor)
                    output.append(test_result)
                elif opcode == 5:
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    if input1 != 0:
                        cursor = input2-1
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 6:
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    if input1 == 0:
                        cursor = input2-1
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 7:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    value = 1 if input1 < input2 else 0
                    memory[memory[cursor+3]] = value
                elif opcode == 8:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    value = 1 if input1 == input2 else 0
                    memory[memory[cursor+3]] = value
                elif opcode == 99:
                    halted = True
                else:
                    raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
            cursor += 1

        return memory, output[0]

    def get_opcode(self, cursor):
        return int(str(self.memory[cursor])[-2:])

    def get_modes(self, cursor):
        return str(self.memory[cursor])[:-2][::-1] + '0000'

    def determine_inputs(self, memory, mode, index):
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

class Amp:
    def __init__(self, memory, input, output=None):
        self.memory = memory
        self.input = input
        self.output = output

    def run(self):
        memory, output = Intcode(self.memory).run()
        self.output = output
        return memory, output


def amp_system(memory, sequence, loop_setting='series'):
    thing = 0
    for phase in sequence:
        amp = Amp(memory, thing)
        _, thing = amp.run()
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
    largest, sequence = puzzle7(memory)
    print(f'7a: {largest}')

    largest, sequence = puzzle7(memory, '56789')
    print(f'7b: {largest}')
