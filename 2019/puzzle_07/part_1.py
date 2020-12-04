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

    def run(self, inputs=None):
        if inputs is None:
            inputs = []
        memory = self.memory

        cursor = 0
        next_instruction = 0
        output = None
        halted = False
        while not halted:
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
                    self.debug(f'mid memory: {pretty_print(memory, [cursor, cursor+1, memory[cursor+1]])}')
                    memory[memory[cursor+1]] = inputs.pop()
                elif opcode == 4:
                    next_instruction += 2
                    test_result, _ = self.determine_inputs(memory, modes, cursor)
                    self.debug(f'output: {test_result}')
                    output = test_result
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
                    raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
                self.debug(f'after memory: {pretty_print(memory, [cursor])}')
            cursor += 1
            self.debug(f'set cursor to {cursor}')

        return memory, output

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

    def run(self):
        memory, output = Intcode(self.memory).run(self.input)
        self.memory = memory
        if output is not None:
            self.output = output
        return memory, self.output

class System:
    def __init__(self):
        self.amps = []
        for amp_name in list('ABCDE'):
            self.amps.append(Amp(name=amp_name))

    def run(self, memory, sequence):
        thing = 0
        for amp, phase in zip(self.amps, sequence):
            amp.memory = memory
            amp.input = [thing, int(phase)]
            _, thing = amp.run()
        return thing

def test_examples():
    system = System()
    memory = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert system.run(memory, '43210') == 43210

    memory = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
              101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert system.run(memory, '01234') == 54321

    memory = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
              1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert system.run(memory, '10432') == 65210

def puzzle7():
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]

    winning_sequence = '00000'
    largest = 0
    for sequence_arr in list(permutations('01234', 5)):
        system = System()
        sequence = ''.join(sequence_arr)
        output = system.run(memory, sequence)
        if output is not None and output > largest:
            largest = output
            winning_sequence = sequence

    print(f'{largest}')

if __name__ == '__main__':
    test_examples()
    puzzle7()
