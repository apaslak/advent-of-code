import pdb
lower_range = 124075
upper_range = 580769


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


count = 0
for number in range(lower_range, upper_range):
    str_number = str(number)
    if validate_sets_of_two(list(str_number)) and validate_never_decrease(str_number):
        count += 1

print(f'count: {count}')

print(f"validate_sets_of_two('111111')  : {validate_sets_of_two('111111') == True}")
print(f"validate_never_decrease('111111'): {validate_never_decrease('111111') == True}")
print(f'-----')
print(f"validate_sets_of_two('223450')  : {validate_sets_of_two('223450') == True}")
print(f"validate_never_decrease('223450'): {validate_never_decrease('223450') == False}")
print(f'-----')
print(f"validate_sets_of_two('123789')  : {validate_sets_of_two('123789') == False}")
print(f"validate_never_decrease('123789'): {validate_never_decrease('123789') == True}")
print(f'-----')
print(f"validate_sets_of_two('112233')  : {validate_sets_of_two('112233') == True}")
print(f"validate_never_decrease('112233'): {validate_never_decrease('112233') == True}")
print(f'-----')
print(f"validate_sets_of_two('123444')  : {validate_sets_of_two('123444') == False}")
print(f"validate_never_decrease('123444'): {validate_never_decrease('123444') == True}")
print(f'-----')
print(f"validate_sets_of_two('111122')  : {validate_sets_of_two('111122') == True}")
print(f"validate_never_decrease('111122'): {validate_never_decrease('111122') == True}")
print(f'-----')

# this got the right answer BUT
# one of the tests fails??????
