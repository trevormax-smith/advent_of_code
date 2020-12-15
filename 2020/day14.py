# Advent of Code 2020, Day 14
# Michael Bell
# 12/14/2020

import math
from itertools import product
from collections import defaultdict
import helper


def dec_to_bin(value):
    binary_value = [0] * 36
    rem = value
    while rem > 0:
        p = int(math.log2(rem))
        binary_value[-p-1] = 1
        rem -= 2 ** p
    return binary_value


def bin_to_dec(binary_value):
    val = 0
    for i, bv in enumerate(binary_value[::-1]):
        val += int(bv) * 2 ** i
    return val


class Initializer(object):
    def __init__(self):
        self.bitmask = ['X'] * 36
        self.memory = defaultdict(lambda x: 0)  # Addressable memory, initialized to zero
    
    def set_bitmask(self, bitmask):
        self.bitmask = bitmask
    
    def apply_mask(self, value):
        binary_value = dec_to_bin(value)
        for i, m in enumerate(self.bitmask):
            if m == 'X':
                continue
            binary_value[i] = int(m)
        value = bin_to_dec(binary_value)
        return value

    def set_memory(self, address, value):
        value = self.apply_mask(value)
        self.memory[address] = value

    def run_program(self, program):
        for line in program:
            if line[:3] == 'mas':
                self.set_bitmask(line.split(' = ')[1])
            elif line[:3] == 'mem':
                reg = int(line.split('[')[1].split(']')[0])
                val = int(line.split(' = ')[1])
                self.set_memory(reg, val)



class InitializerV2(Initializer):
    def __init__(self):
        super().__init__()
    
    def apply_mask(self, value):
        bin_val = dec_to_bin(value)
        for i, m in enumerate(self.bitmask):
            if m == 'X':
                bin_val[i] = 'X'
            elif m == '1':
                bin_val[i] = '1'
            else:
                bin_val[i] = str(bin_val[i])
        return bin_val

    def set_memory(self, address, value):
        masked_address = self.apply_mask(address)
        floating_indices = [i for i, v in enumerate(masked_address) if v == 'X']
        floating_combos = [val for val in product('01', repeat=len(floating_indices))]
        
        for floating_combo in floating_combos:
            this_masked_address = [ma for ma in masked_address]
            for i, fi in enumerate(floating_indices):
                this_masked_address[fi] = floating_combo[i]
            this_address = bin_to_dec(this_masked_address)
            self.memory[this_address] = value


### TESTS ###############################
sample_program = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''.split('\n')

initializer = Initializer()
initializer.run_program(sample_program)
assert sum(initializer.memory.values()) == 165

sample_program = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''.split('\n')

initializer = InitializerV2()
initializer.run_program(sample_program)
assert sum(initializer.memory.values()) == 208

### THE REAL THING ######################
program = helper.read_input_lines(14)
initializer = Initializer()
initializer.run_program(program)
print('Part 1:', sum(initializer.memory.values()))
initializer = InitializerV2()
initializer.run_program(program)
print('Part 2:', sum(initializer.memory.values()))
