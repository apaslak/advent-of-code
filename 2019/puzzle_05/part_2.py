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

    return memory, output

def puzzle5():
    with open(r'input.txt', 'r') as file:
        memory = [int(instruction) for instruction in file.readline().strip().split(',')]
    memory, output = run(memory, 5)
    print(f'{output}')

def test_examples():
    memory = [3,9,8,9,10,9,4,9,99,-1,8]
    _, output = run(memory, 8)
    assert output == [1]
    _, output = run(memory, 7)
    assert output == [0]
    _, output = run(memory, 9)
    assert output == [0]

    memory = [3,9,7,9,10,9,4,9,99,-1,8]
    _, output = run(memory, 7)
    assert output == [1]
    _, output = run(memory, 8)
    assert output == [0]
    _, output = run(memory, 9)
    assert output == [0]

    memory = [3,3,1108,-1,8,3,4,3,99]
    _, output = run(memory, 8)
    assert output == [1]
    _, output = run(memory, 7)
    assert output == [0]
    _, output = run(memory, 9)
    assert output == [0]

    memory = [3,3,1107,-1,8,3,4,3,99]
    _, output = run(memory, 7)
    assert output == [1]
    _, output = run(memory, 8)
    assert output == [0]
    _, output = run(memory, 9)
    assert output == [0]

    memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    _, output = run(memory, 0)
    assert output == [0]
    _, output = run(memory, 8)
    assert output == [1]

    memory = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    _, output = run(memory, 0)
    assert output == [0]
    _, output = run(memory, 8)
    assert output == [1]

    memory = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
              1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
              999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    _, output = run(memory, 7)
    assert output == [999]
    _, output = run(memory, 8)
    assert output == [1000]
    _, output = run(memory, 9)
    assert output == [1001]

if __name__ == '__main__':
    test_examples()
    puzzle5()
