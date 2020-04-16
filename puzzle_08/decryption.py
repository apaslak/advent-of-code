import pdb

def calculate_layers(x, y, input_len):
    return int(input_len / (x * y))

def divide_by_layer(code, x, y):
    layer_size = x * y
    num_layers = calculate_layers(x, y, len(code))
    layers = []
    cursor = 0
    for _ in range(0, num_layers):
        layers.append(code[cursor:layer_size+cursor])
        cursor += layer_size

    return layers

def fewest_zeros(layers):
    chosen_layer = layers[0]
    for layer in layers:
        if layer.count('0') < chosen_layer.count('0'):
            chosen_layer = layer

    return chosen_layer

def print_pic(result, x, y):
    cursor = 0
    for _ in range(0, y):
        print(result[cursor:x+cursor])
        cursor += x

def decrypt(layers):
    code = ''
    for pixel in zip(*layers):
        code += determine_pixel_color(pixel)
    return code

def determine_pixel_color(pixel):
    color = None
    for i in range(len(pixel)):
        if pixel[i] == '0':
            color = ' ' # 0
            break
        elif pixel[i] == '1':
            color = '1'
            break
        elif pixel[i] == '2':
            color = '2'
    return color

def test_determine_pixel_color():
    assert determine_pixel_color(tuple('121')) == '1'
    assert determine_pixel_color(tuple('212')) == '1'
    assert determine_pixel_color(tuple('2201')) == '0'
    assert determine_pixel_color(tuple('2222')) == '2'

def test1():
    code = '123456789012'
    layers = divide_by_layer(code, 3, 2)
    fewest_zeros_layer = fewest_zeros(layers)
    print(f"fewest_zeros(layers): { fewest_zeros_layer == '123456'}")
    result = fewest_zeros_layer.count('1') * fewest_zeros_layer.count('2')
    print(f'test1(): {result == 1}')

def test2():
    code = '0222112222120000'
    layers = divide_by_layer(code, 2, 2)
    result = decrypt(layers)
    print(f"test2(): {result == '0110'}")
    print_pic(result, 2, 2)

def puzzle8():
    with open(r'input.txt', 'r') as file:
        code = file.readline().strip()

    layers = divide_by_layer(code, 25, 6)
    fewest_zeros_layer = fewest_zeros(layers)
    result = fewest_zeros_layer.count('1') * fewest_zeros_layer.count('2')
    print(f'8a: {result}')

    result = decrypt(layers)
    print(f'8b:')
    print_pic(result, 25, 6)

if __name__ == '__main__':
    test1()
    test2()
    puzzle8()
