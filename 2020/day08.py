# Advent of Code 2020, Day 8
# Michael Bell
# 12/8/2020
import helper

class InfiniteLoopError(Exception):
    pass


def compile_program(program_code):
    output = []
    for line in program_code:
        cmd, arg = line.split(' ')
        output.append((cmd, int(arg.replace('+', ''))))
    return output


class Interpreter(object):

    def __init__(self):
        self.reset()
    
    def execute_program(self, program):
        self.reset()
        step = 1
        n_lines = len(program)

        while self.position < n_lines:
            if self.position not in self.execution_order:
                self.execution_order[self.position] = step
                self.execute_command(*program[self.position])
            else:
                raise InfiniteLoopError(
                    f'Infinite loop detected at step {step}, line {self.position}. Accumulator value {self.accumulator}.'
                )
            step += 1

        return

    def reset(self):
        self.execution_order = {}
        self.accumulator = 0
        self.position = 0

    def play_back(self):
        exor = sorted([(interp.execution_order[k], k) for k in interp.execution_order], key=lambda x: x[0])
        for line in exor:
            print(line[0], line[1] + 1)  # Adding 1 to the code line because line numbering in editor starts at 1

    def execute_command(self, cmd, arg):
        getattr(self, cmd)(arg)

    def nop(self, arg):
        self.position += 1
        return
    
    def acc(self, arg):
        self.accumulator += arg
        self.position += 1
        return
    
    def jmp(self, arg):
        self.position += arg
        return


def fix_program(program):
    interp = Interpreter()

    for i, loc in enumerate(program):

        cmd, arg = loc
        if loc[0] == 'nop':
            cmd = 'jmp'
        elif loc[0] == 'jmp':
            cmd = 'nop'
        else:
            continue
        
        new_program = program[:i] + [(cmd, arg)] + program[i+1:]

        try:
            interp.execute_program(new_program)
        except InfiniteLoopError:
            continue
        
        return new_program


sample_program = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''.split('\n')

sample_program = compile_program(sample_program)

interp = Interpreter()
try:
    interp.execute_program(sample_program)
except InfiniteLoopError:
    interp.play_back()
    assert interp.accumulator == 5

fixed_sample_program = fix_program(sample_program)
print(fixed_sample_program)
interp.execute_program(fixed_sample_program)
assert interp.accumulator == 8

program = compile_program(helper.read_input_lines(8))
interp = Interpreter()
try:
    interp.execute_program(program)
except InfiniteLoopError:
    print('Accumulator at infinite loop:', interp.accumulator)

fixed_program = fix_program(program)
interp.execute_program(fixed_program)
print('Accumulator on successful execution:', interp.accumulator)
