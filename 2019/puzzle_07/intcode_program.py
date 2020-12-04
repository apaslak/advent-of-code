import pdb
from itertools import permutations

def pretty_print(memory, cursors=None):
    if cursors is None:
        cursors = []
    pretty_memory = '['
    for i, point in enumerate(memory):
        if i in cursors:
            pretty_memory += f"<{point}>, "
        else:
            pretty_memory += f"{point}, "

    pretty_memory += "]"
    return pretty_memory

class Intcode:
    def __init__(self, memory):
        self.memory = memory.copy()

    def run(self, inputs=None, cursor=None):
        if inputs is None:
            inputs = []
        if cursor is None:
            cursor = 0
        memory = self.memory

        next_instruction = cursor
        output = None
        halted = False
        paused = False
        while not halted and not paused:
            if cursor == next_instruction:
                opcode = self.get_opcode(cursor)
                modes = self.get_modes(cursor)
                self.debug(f'opcode: {opcode}, cursor: {cursor}')
                self.debug(f'before memory: {pretty_print(memory, [cursor])}')
                if opcode == 1:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+3, memory[cursor+3]])}')
                    memory[memory[cursor+3]] = input1 + input2
                elif opcode == 2:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+3, memory[cursor+3]])}')
                    memory[memory[cursor+3]] = input1 * input2
                elif opcode == 3:
                    next_instruction += 2
                    # selected_input = input("Enter input: ")
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+1, memory[cursor+1]])}')
                    memory[memory[cursor+1]] = inputs.pop()
                elif opcode == 4:
                    next_instruction += 2
                    test_result, _ = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'========= paused =========')
                    self.debug(f'output: {test_result}')
                    self.debug(f'========= paused =========')
                    output = test_result
                    paused = True
                elif opcode == 5:
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'input1: {input1}, input2: {input2}')
                    if input1 != 0:
                        cursor = input2-1
                        self.debug(f'set cursor to {cursor}')
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 6:
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'input1: {input1}, input2: {input2}')
                    if input1 == 0:
                        cursor = input2-1
                        self.debug(f'set cursor to {cursor}')
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 7:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    value = 1 if input1 < input2 else 0
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+3, memory[cursor+3]])}')
                    memory[memory[cursor+3]] = value
                elif opcode == 8:
                    next_instruction += 4
                    input1, input2 = self.determine_inputs(memory, modes, cursor)
                    value = 1 if input1 == input2 else 0
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+3, memory[cursor+3]])}')
                    memory[memory[cursor+3]] = value
                elif opcode == 99:
                    self.debug(f'========= halted =========')
                    halted = True
                else:
                    pdb.set_trace()
                    raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
                self.debug(f'after memory: {pretty_print(memory, [cursor])}')
            cursor += 1
            self.debug(f'set cursor to {cursor}')

        return memory, output, cursor+1, halted

    def get_opcode(self, cursor):
        return int(str(self.memory[cursor])[-2:])

    def get_modes(self, cursor):
        return str(self.memory[cursor])[:-2][::-1] + '0000'

    def determine_inputs(self, memory, mode, cursor):
        if mode[0] == '0':
            input1 = memory[memory[cursor+1]]
        else:
            input1 = memory[cursor+1]

        try:
            if mode[1] == '0':
                input2 = memory[memory[cursor+2]]
            else:
                input2 = memory[cursor+2]
        except:
            input2 = None

        return input1, input2

    def debug(self, whatever, force=False):
        if force:
            print(whatever)

class Amp:
    def __init__(self, name, memory=None, input=None, output=None):
        self.name = name
        self.memory = memory
        self.input = input
        self.output = output
        self.cursor = 0

    def run(self):
        memory, output, cursor, halted = Intcode(self.memory).run(self.input, self.cursor)
        self.memory = memory
        if output is not None:
            self.output = output
        self.cursor = cursor
        return memory, self.output, halted

class System:
    def __init__(self, loop_setting='series'):
        self.amps = []
        for amp_name in list('ABCDE'):
            self.amps.append(Amp(name=amp_name))
        self.loop_setting = loop_setting

    def run(self, memory, sequence):
        thing = 0
        for amp, phase in zip(self.amps, sequence):
            amp.memory = memory
            amp.input = [thing, int(phase)]
            _, thing, _ = amp.run()
        if self.loop_setting == 'feedback':
            halted = False
            while not halted:
                for amp in self.amps:
                    amp.input = [thing]
                    _, thing, halted = amp.run()
        return thing


def puzzle7(memory, phase_settings='01234', loop_setting='series'):
    winning_sequence = '00000'
    largest = 0
    for sequence_arr in list(permutations(phase_settings, len(phase_settings))):
        system = System(loop_setting=loop_setting)
        sequence = ''.join(sequence_arr)
        output = system.run(memory, sequence)
        if output is not None and output > largest:
            largest = output
            winning_sequence = sequence

    return largest, winning_sequence

if __name__ == '__main__':
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]
    largest, sequence = puzzle7(memory)
    print(f'7a: {largest}')

    largest, sequence = puzzle7(memory, phase_settings='56789', loop_setting='feedback')
    print(f'7b: {largest}')
