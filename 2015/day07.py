# Advent of Code 2015, Day 7
# Michael Bell
# 1/3/2021

import helper


# Python doesn't have a uint16, but this will convert a Python int to the uint16 value
# From https://gist.github.com/coolharsh55/711360947b40e8cc404e
uint16 = lambda x: x & 0xFFFF


def parse_instructions(instructions):
    wire_instructions = {}
    for instruction in instructions:
        signal_source, target_wire = instruction.split(' -> ')
        wire_instructions[target_wire] = signal_source
    return wire_instructions


class Circuit(object):

    def __init__(self, instructions):
        self.instructions = parse_instructions(instructions)
        self.wire_values = {}

    def get_signal(self, val):
        try:

            val = int(val)
            return val

        except ValueError:
            
            if val not in self.wire_values:

                instructions = self.instructions[val]

                try:
                    to_set = int(instructions)
                except ValueError:
                    instruction_parts = instructions.split(' ')
                    if len(instruction_parts) == 1:
                        to_set = self.get_signal(instruction_parts[0])
                    elif len(instruction_parts) == 2:
                        to_set = self.not_op(self.get_signal(instruction_parts[1]))
                    else:
                        l_arg, op_name, r_arg = instruction_parts
                        to_set = getattr(self, op_name.lower() + '_op')(
                            self.get_signal(l_arg), 
                            self.get_signal(r_arg)
                        )
                
                self.wire_values[val] = to_set
            
            return self.wire_values[val]

    def and_op(self, left, right):
        return uint16(left & right)
    def or_op(self, left, right):
        return uint16(left | right)
    def not_op(self, val):
        return uint16(~val)
    def rshift_op(self, val, shift):
        return uint16(val >> shift)
    def lshift_op(self, val, shift):
        return uint16(val << shift)


example_instructions = '''123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i'''.split('\n')

sample_circuit = Circuit(example_instructions)
assert sample_circuit.get_signal('d') == 72
assert sample_circuit.get_signal('e') == 507
assert sample_circuit.get_signal('f') == 492
assert sample_circuit.get_signal('g') == 114
assert sample_circuit.get_signal('h') == 65412
assert sample_circuit.get_signal('i') == 65079
assert sample_circuit.get_signal('x') == 123
assert sample_circuit.get_signal('y') == 456

instructions = helper.read_input_lines(7)
circuit = Circuit(instructions)
wire_a = circuit.get_signal('a')
print('Part 1:', wire_a)

circuit = Circuit(instructions)
circuit.wire_values['b'] = wire_a
print('Part 2:', circuit.get_signal('a'))
