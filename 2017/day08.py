# Code for the 2017 Advent Of Code, day 8
# http://adventofcode.com/2017
# Michael Bell
# 12/14/2017
# Solutions validated

from collections import defaultdict
import operator


def get_operator(op_string):
    if op_string == '>':
        op = operator.gt
    elif op_string == '>=':
        op = operator.ge
    elif op_string == "<":
        op = operator.lt
    elif op_string == "<=":
        op = operator.le
    elif op_string == "==":
        op = operator.eq
    elif op_string == "!=":
        op = operator.ne
    else:
        raise ValueError("Invalid operator")

    return op

def parse_line(instructions):
    tokens = instructions.split()
       
    register = tokens[0]
    modifier = int(tokens[2])
    if tokens[1] == 'dec':
        modifier *= -1

    condition_register = tokens[4]
    condition_value = int(tokens[6])
    op = get_operator(tokens[5])

    return {'reg': register, 'mod': modifier, 'creg': condition_register, 
            'cval': condition_value, 'op': op}


class CPU(object):
    def __init__(self):
        self.registers = defaultdict(int)

    def run_line(self, instructions):
        """
        Parse a line of instructions and return the register to alter and the 
        number to add to the register.
        """
        
        inst = parse_line(instructions)
        
        if not inst['op'](self.registers[inst['creg']], inst['cval']):
            inst['mod'] = 0

        self.registers[inst['reg']] += inst['mod']

    def run_lines(self, lines):
        """
        """
        lines = lines.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            self.run_line(line)

    def get_max_register_value(self):
        return max(self.registers[reg] for reg in self.registers)

def highest_register_value(instructions):

    lines = instructions.split('\n')
    max_val = -1
    cpu = CPU()
    for line in lines:
        if len(line) == 0:
            continue
        cpu.run_line(line)
        current_max = cpu.get_max_register_value()
        if current_max > max_val:
            max_val = current_max 
    return max_val

test_instructions = '''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''

with open('data/day08_input.txt', 'r') as f:
    puzzle_instructions = f.read().replace('\r', '')

if __name__ == '__main__':
    # TESTS 
    cpu = CPU()
    cpu.run_lines(test_instructions)
    assert cpu.get_max_register_value() == 1
    assert highest_register_value(test_instructions) == 10
    print("All tests passed!")  

    cpu = CPU()
    cpu.run_lines(puzzle_instructions)
    print("Solution 1: {:}".format(cpu.get_max_register_value()))
    print("Solution 2: {:}".format(highest_register_value(puzzle_instructions)))
