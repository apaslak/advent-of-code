import pdb
from itertools import permutations

class Disk:
    def __init__(self, memory):
        self.memory = memory.copy()

    def __getitem__(self, position):
        try:
            return self.memory[position]
        except:
            self._expand_to(position)

            return self.memory[position]

    def __setitem__(self, position, value):
        try:
            self.memory[position] = value
        except:
            self._expand_to(position)
            self.memory[position] = value

    def pretty_print(self, cursors=None):
        if cursors is None:
            cursors = []
        pretty_memory = '['
        for i, point in enumerate(self.memory):
            if i in cursors:
                pretty_memory += f"<{point}>, "
            else:
                pretty_memory += f"{point}, "

        pretty_memory += "]"
        return pretty_memory

    def _expand_to(self, position):
        memory_length = len(self.memory)
        if position >= memory_length:
            addition = [0] * (position+1-memory_length)
            self.memory += addition

class Intcode:
    def __init__(self, memory):
        self.memory = Disk(memory)

    def run(self, inputs=None, cursor=None):
        if inputs is None:
            inputs = []
        if cursor is None:
            cursor = 0
        memory = self.memory

        next_instruction = cursor
        relative_base = cursor
        output = []
        halted = False
        while not halted:
            if cursor == next_instruction:
                opcode = self.get_opcode(cursor)
                modes = self.get_modes(cursor)
                self.debug(f'opcode: {opcode}, cursor: {cursor}')
                self.debug(f'before memory: {memory.pretty_print([cursor])}')
                if opcode == 1:
                    next_instruction += 4
                    input1, input2, destination = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    self.debug(f'mid memory: {memory.pretty_print([cursor, cursor+3, memory[cursor+3]])}')
                    memory[destination] = input1 + input2
                elif opcode == 2:
                    next_instruction += 4
                    input1, input2, destination = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    self.debug(f'mid memory: {memory.pretty_print([cursor, cursor+3, memory[cursor+3]])}')
                    memory[destination] = input1 * input2
                elif opcode == 3:
                    next_instruction += 2
                    self.debug(f'mid memory: {memory.pretty_print([cursor, cursor+1, memory[cursor+1]])}')
                    destination, _, _ = self.determine_values(modes, cursor, relative_base)
                    memory[destination] = inputs.pop()
                elif opcode == 4:
                    next_instruction += 2
                    test_result, _, _ = self.determine_values(modes, cursor, relative_base)
                    test_result = memory[test_result]
                    self.debug(f'output: {test_result}')
                    output.append(test_result)
                elif opcode == 5:
                    input1, input2, _ = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    self.debug(f'input1: {input1}, input2: {input2}')
                    if input1 != 0:
                        cursor = input2-1
                        self.debug(f'set cursor to {cursor}')
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 6:
                    input1, input2, _ = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    self.debug(f'input1: {input1}, input2: {input2}')
                    if input1 == 0:
                        cursor = input2-1
                        self.debug(f'set cursor to {cursor}')
                        next_instruction = input2
                    else:
                        next_instruction += 3
                elif opcode == 7:
                    next_instruction += 4
                    input1, input2, destination = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    value = 1 if input1 < input2 else 0
                    self.debug(f'mid memory: {memory.pretty_print([cursor, cursor+3, memory[cursor+3]])}')
                    memory[destination] = value
                elif opcode == 8:
                    next_instruction += 4
                    input1, input2, destination = self.determine_values(modes, cursor, relative_base)
                    input1, input2 = memory[input1], memory[input2]
                    value = 1 if input1 == input2 else 0
                    self.debug(f'mid memory: {memory.pretty_print([cursor, cursor+3, memory[cursor+3]])}')
                    memory[destination] = value
                elif opcode == 9:
                    next_instruction += 2
                    input1, _, _ = self.determine_values(modes, cursor, relative_base)
                    input1 = memory[input1]
                    self.debug(f'relative_base updated from {relative_base} to {relative_base + input1}')
                    relative_base += input1
                elif opcode == 99:
                    self.debug(f'========= halted =========')
                    halted = True
                else:
                    pdb.set_trace()
                    raise ValueError(f'opcode: {opcode}, cursor: {cursor}')
                self.debug(f'after memory: {memory.pretty_print([cursor])}')
            cursor += 1
            self.debug(f'set cursor to {cursor}')
            self.debug(f'current output: {output}')

        return memory, output, cursor+1, halted

    def get_opcode(self, cursor):
        return int(str(self.memory[cursor])[-2:])

    def get_modes(self, cursor):
        return str(self.memory[cursor])[:-2][::-1] + '0000'

    def determine_values(self, mode, cursor, relative_base):
        values = []
        for i in [0,1,2]:
            try:
                if mode[i] == '0':
                    values.append(self._mode_zero(self.memory, cursor+i+1))
                elif mode[i] == '1':
                    values.append(self._mode_one(self.memory, cursor+i+1))
                elif mode[i] == '2':
                    values.append(self._mode_two(self.memory, cursor+i+1, relative_base))
            except:
                values.append(None)

        return values

    def _mode_zero(self, memory, cursor):
        return memory[cursor]

    def _mode_one(self, memory, cursor):
        return cursor

    def _mode_two(self, memory, cursor, relative_base):
        return relative_base+memory[cursor]

    def debug(self, whatever, force=False):
        if force:
            print(whatever)

def test_modes():
    intcode = Intcode([])
    assert intcode._mode_zero([1,2,3,4,5], 1) == 2
    assert intcode._mode_zero([1,3,5,7,2], 4) == 2
    assert intcode._mode_zero([0,4,3,1,6], 3) == 1

    assert intcode._mode_one([1,2,3,4,5], 1) == 1
    assert intcode._mode_one([1,3,5,7,2], 4) == 4
    assert intcode._mode_one([0,4,3,1,6], 3) == 3

    assert intcode._mode_two([1,2,3,4,5], 1, 0) == 2
    assert intcode._mode_two([1,3,5,1,2,7,9], 2, 1) == 6
    assert intcode._mode_two([0,4,3,3,6], 3, -2) == 1


def test_examples():
    memory = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    _, output, _, _ = Intcode(memory).run()
    assert output == memory

    memory = [1102,34915192,34915192,7,4,7,99,0]
    _, output, _, _ = Intcode(memory).run()
    assert len(str(output[0])) == 16


    memory = [104,1125899906842624,99]
    _, output, _, _ = Intcode(memory).run()

    assert output == [1125899906842624]

def puzzle9():
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]

    _, output, _, _ = Intcode(memory).run(inputs=[1])
    print(f'9a: {output}')

    _, output, _, _ = Intcode(memory).run(inputs=[2])
    print(f'9b: {output}')

if __name__ == '__main__':
    test_modes()
    test_examples()
    puzzle9()
