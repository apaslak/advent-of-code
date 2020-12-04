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

def test_examples():
    code = '123456789012'
    layers = divide_by_layer(code, 3, 2)
    fewest_zeros_layer = fewest_zeros(layers)
    assert fewest_zeros_layer == '123456'
    assert (fewest_zeros_layer.count('1') * fewest_zeros_layer.count('2')) == 1

def puzzle8():
    with open(r'input.txt', 'r') as file:
        code = file.readline().strip()

    layers = divide_by_layer(code, 25, 6)
    fewest_zeros_layer = fewest_zeros(layers)
    result = fewest_zeros_layer.count('1') * fewest_zeros_layer.count('2')
    print(f'8a: {result}')

if __name__ == '__main__':
    test_examples()
    puzzle8()
