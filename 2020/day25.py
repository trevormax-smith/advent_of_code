# Advent of Code 2020, Day 25
# Michael Bell
# 12/25/2020

import helper


divisor = 20201227


def transform(subject_number, loop_size):
    value = 1

    for _ in range(loop_size):
        value *= subject_number
        value = value % divisor
    
    return value


def infer_loop_size(public_key):
    loop_size = 1
    value = 1

    while True:
        
        value *= 7
        value = value % divisor
        if value == public_key:
            return loop_size
        if loop_size % 10_000 == 0:
            print(loop_size, value)
        loop_size += 1


assert transform(7, 8) == 5764801
assert transform(7, 11) == 17807724
assert infer_loop_size(5764801) == 8
assert infer_loop_size(17807724) == 11

assert transform(17807724, 8) == transform(5764801, 11)
assert transform(17807724, 8) == 14897079

public_keys = [int(k) for k in helper.read_input_lines(25)]

loop_size = infer_loop_size(public_keys[0])

print('Part 1:', transform(public_keys[1], loop_size))
