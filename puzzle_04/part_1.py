import pdb

def validate_sets_of_two(chars):
    for i in range(1, len(chars)):
        if chars[i-1] == chars[i]:
            return True
    return False

def validate_never_decrease(number):
    chars = list(number)
    for i in range(0, len(chars)-1):
        if int(chars[i]) > int(chars[i+1]):
            return False

    return True

def test_examples():
    assert validate_sets_of_two('111111') == True
    assert validate_sets_of_two('223450') == True
    assert validate_sets_of_two('123789') == False

    assert validate_never_decrease('111111') == True
    assert validate_never_decrease('223450') == False
    assert validate_never_decrease('123789') == True

def puzzle4():
    count = 0
    for number in range(124075, 580769):
        str_number = str(number)
        if validate_sets_of_two(list(str_number)) and validate_never_decrease(str_number):
            count += 1

    print(f'{count}')

if __name__ == '__main__':
    test_examples()
    puzzle4()
