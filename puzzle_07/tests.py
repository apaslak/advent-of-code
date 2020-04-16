# from intcode import intcode, puzzle7
from intcode_program import System, puzzle7

def test_one():
    memory = [3,9,8,9,10,9,4,9,99,-1,8]
    results = True
    _, output = intcode(memory, 8)
    results = results and output == 1
    _, output = intcode(memory, 7)
    results = results and output == 0
    _, output = intcode(memory, 9)
    results = results and output == 0
    print(f'test_one: {results}')

def test_two():
    memory = [3,9,7,9,10,9,4,9,99,-1,8]
    results = True
    _, output = intcode(memory, 7)
    results = results and output == 1
    _, output = intcode(memory, 8)
    results = results and output == 0
    _, output = intcode(memory, 9)
    results = results and output == 0
    print(f'test_two: {results}')

def test_three():
    memory = [3,3,1108,-1,8,3,4,3,99]
    results = True
    _, output = intcode(memory, 8)
    results = results and output == 1
    _, output = intcode(memory, 7)
    results = results and output == 0
    _, output = intcode(memory, 9)
    results = results and output == 0
    print(f'test_three: {results}')

def test_four():
    memory = [3,3,1107,-1,8,3,4,3,99]
    results = True
    _, output = intcode(memory, 7)
    results = results and output == 1
    _, output = intcode(memory, 8)
    results = results and output == 0
    _, output = intcode(memory, 9)
    results = results and output == 0
    print(f'test_four: {results}')

def test_five():
    memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    results = True
    _, output = intcode(memory, 0)
    results = results and output == 0
    _, output = intcode(memory, 8)
    results = results and output == 1

    memory = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    _, output = intcode(memory, 0)
    results = results and output == 0
    _, output = intcode(memory, 8)
    results = results and output == 1
    print(f'test_five: {results}')

def test_six():
    memory = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
              1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
              999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    results = True
    _, output = intcode(memory, 7)
    results = results and output == 999
    _, output = intcode(memory, 8)
    results = results and output == 1000
    _, output = intcode(memory, 9)
    results = results and output == 1001
    print(f'test_six: {results}')

def test_seven():
    memory = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    largest, sequence = puzzle7(memory)
    print(f"test_seven: largest: {largest == 43210}, sequence: {sequence == '43210'}")

    memory = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
    largest, sequence = puzzle7(memory)
    print(f"test_seven: largest: {largest == 54321}, sequence: {sequence == '01234'}")

    memory = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,
              31,4,31,99,0,0,0]
    largest, sequence = puzzle7(memory)
    print(f"test_seven: largest: {largest == 65210}, sequence: {sequence == '10432'}")

def test_eight():
    memory = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
              27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    largest, sequence = puzzle7(memory, phase_settings='56789', loop_setting='feedback')
    print(f"test_eight: largest: {largest == 139629729}, sequence: {sequence == '98765'}")

    memory = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
              -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
              53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    largest, sequence = puzzle7(memory, phase_settings='56789', loop_setting='feedback')
    print(f"test_eight: largest: {largest == 18216}, sequence: {sequence == '97856'}")


if __name__ == '__main__':
    # test_one()
    # test_two()
    # test_three()
    # test_four()
    # test_five()
    # test_six()
    # test_seven()
    test_eight()
