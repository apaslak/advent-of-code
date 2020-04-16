import pdb
lower_range = 124075
upper_range = 580769


def validate_double_digit_recursive(chars, any_doubles=False, last_char=None, counter=0):
    if len(chars) == 0 and last_char is None and counter == 0:
        return any_doubles

    if last_char is None:
        return validate_double_digit_recursive(chars[1:], any_doubles, chars[0], counter+1)
    elif len(chars) > 0 and chars[0] == last_char:
        return validate_double_digit_recursive(chars[1:], True, chars[0], counter+1)
    else:
        if counter % 2 == 0 or counter == 1:
            return validate_double_digit_recursive(chars, any_doubles)
        else:
            return False


def validate_double_digit_iter(chars):
    last_char = chars[0]
    counter = 1
    double_found = False
    for i in range(1, len(chars)):
        if last_char == chars[i]:
            counter += 1
            double_found = True
            if i == len(chars)-1:
                if counter % 2 != 0:
                    double_found = False
        else:
            if counter % 2 == 0 or counter == 1:
                counter = 1
                last_char = chars[i]
                # this is fine
            else:
                double_found = False
                break

    return double_found

def validate_sets_of_two(chars):
    for i in range(0, len(chars)-1):
        check_left = i == 0 or chars[i-1] != chars[i]
        check_right = i+1 == len(chars)-1 or chars[i+2] != chars[i+1]
        if chars[i] == chars[i+1] and check_left and check_right:
            return True
    return False


def validate_never_decrease(number):
    chars = list(number)
    for i in range(0, len(chars)-1):
        if int(chars[i]) > int(chars[i+1]):
            return False

    return True


def intersection(lst2, lst1):
    return set(lst2).intersection(lst1)

def diff(li1, li2):
    return (list(set(li1) - set(li2)))


iter_count = 0
recursive_count = 0
blah_count = 0
for number in range(lower_range, upper_range):
    str_number = str(number)
    if validate_double_digit_iter(list(str_number)) and validate_never_decrease(str_number):
        iter_count += 1
    if validate_double_digit_recursive(list(str_number)) and validate_never_decrease(str_number):
        recursive_count += 1
    if validate_sets_of_two(list(str_number)) and validate_never_decrease(str_number):
        blah_count += 1

print(f'iter_count: {iter_count}')
print(f'recursive_count: {recursive_count}')
print(f'blah_count: {blah_count}')

def run_tests(method):
    print(f"{method}('111111')  : {method('111111') == True}")
    print(f"validate_never_decrease('111111'): {validate_never_decrease('111111') == True}")
    print(f'-----')
    print(f"{method}('223450')  : {method('223450') == True}")
    print(f"validate_never_decrease('223450'): {validate_never_decrease('223450') == False}")
    print(f'-----')
    print(f"{method}('123789')  : {method('123789') == False}")
    print(f"validate_never_decrease('123789'): {validate_never_decrease('123789') == True}")
    print(f'-----')
    print(f"{method}('112233')  : {method('112233') == True}")
    print(f"validate_never_decrease('112233'): {validate_never_decrease('112233') == True}")
    print(f'-----')
    print(f"{method}('123444')  : {method('123444') == False}")
    print(f"validate_never_decrease('123444'): {validate_never_decrease('123444') == True}")
    print(f'-----')
    print(f"{method}('111122')  : {method('111122') == True}")
    print(f"validate_never_decrease('111122'): {validate_never_decrease('111122') == True}")
    print(f'-----')

run_tests(validate_double_digit_recursive)
run_tests(validate_double_digit_iter)
