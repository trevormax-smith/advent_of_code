# Code for the 2018 AoC, day 16
# https://adventofcode.com/2018/day/16
# Michael Bell
# 12/16/2018


class Device(object):
    ops = [
        'addr',
        'addi',
        'mulr',
        'muli', 
        'banr',
        'bani',
        'borr',
        'bori',
        'setr',
        'seti',
        'gtir',
        'gtri',
        'gtrr',
        'eqir',
        'eqri',
        'eqrr'
    ]
    def __init__(self, op_map = None):
        self.registers = [0] * 4
        self.op_map = op_map
    def execute_program(self, program):
        if self.op_map is None:
            raise Exception("Must initialize with an op code to op map!")
        for line in program:
            getattr(self, self.op_map[line[0]])(*line[1:])
    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]
    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b
    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]
    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b
    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]
    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b
    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]
    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b
    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]
    def seti(self, a, b, c):
        self.registers[c] = a
    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0
    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0
    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0
    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0
    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0
    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0
    

def parse_reg_line(reg_line):
    return [int(val) for val in reg_line.split('[')[1].replace(']', '').split(',')]


def parse_instructions(instr_line):
    return [int(val) for val in instr_line.split()]


def parse_tests(test_input):
    sample_ops = []
    test_program = []

    parsing_samples = True
    start_reg = None
    end_reg = None
    instr = None

    lines = test_input.split('\n')

    for line in lines:
        if "Before" in line:
            start_reg = parse_reg_line(line)
        elif "After" in line:
            end_reg = parse_reg_line(line)
            sample_ops.append({
                'start_reg': start_reg, 
                'instructions': instr, 
                'end_reg': end_reg
            })
            start_reg = None
            end_reg = None
            instr = None
        elif parsing_samples and start_reg is not None:
            instr = parse_instructions(line)
        elif len(line) == 0:
            continue
        else:
            test_program.append(parse_instructions(line))

    return sample_ops, test_program


def find_possible_ops(start_reg, end_reg, instr):
    dev = Device()

    possible_ops = []

    for op in dev.ops:
        dev.registers = [val for val in start_reg]
        getattr(dev, op)(*instr[1:])
        if dev.registers == end_reg:
            possible_ops.append(op)

    return possible_ops


def assign_possible_ops(test_ops):

    for test_op in test_ops:
        test_op['pops'] = find_possible_ops(
            test_op['start_reg'],
            test_op['end_reg'],
            test_op['instructions']
        )


def opcode_to_op(ops):

    op_codes = list(set(op['instructions'][0] for op in ops))
    op_map = {}

    for op_code in op_codes:
        matching_ops = None
        for op in ops:
            if op['instructions'][0] == op_code:
                if matching_ops is None:
                    matching_ops = set(op['pops'])
                else:
                    matching_ops = matching_ops.intersection(set(op['pops']))
        op_map[op_code] = list(matching_ops)

    matched_ops = []
    op_map2 = {}
    while len(op_map) > 0:
        unique_matches = [k for k in op_map if len(op_map[k]) == 1]
        for unique_match in unique_matches:
            op_map2[unique_match] = op_map.pop(unique_match)[0]
            for k in op_map:
                if op_map2[unique_match] in op_map[k]:
                    op_map[k].remove(op_map2[unique_match])

    return op_map2


if __name__ == '__main__':

    with open('./data/day16_input.txt', 'r') as f:
        input1 = f.read()

    ops, prg = parse_tests(input1)

    pops = find_possible_ops([3, 2, 1, 1], [3, 2, 2, 1], [9, 2, 1, 2])
    assert len(pops) == 3 and 'mulr' in pops and 'addi' in pops and 'seti' in pops

    assign_possible_ops(ops)

    print(f'Solution 1: {sum(1 for op in ops if len(op["pops"]) >= 3)}')

    op_map = opcode_to_op(ops)

    dev = Device(op_map)
    dev.execute_program(prg)
    print(f'Solution 2: {dev.registers[0]}')
