"""
2017 Advent Of Code, day 18
https://adventofcode.com/2017/day/18
Michael Bell
12/22/2017
Solutions passed
**GAHD this is ugly tho**
"""

import asyncio
from asyncio.queues import Queue


class SoundCard(object):
    def __init__(self):
        self.registers = [0] * 26
        self.register_names = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
        self.last_sound = None

    def get_register(self, reg):
        return self.registers[self.reg_index(reg)]

    def reg_index(self, reg):
        return self.register_names.index(reg)
    
    def set_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] = val

    def multiply_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] *= val

    def modulo_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] = self.registers[ndx] % val

    def play_sound(self, reg):
        if reg.isdigit():
            self.last_sound = int(reg)
        else:
            self.last_sound = self.get_register(reg)
    
    def add_to_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] += val

    def _get_op_params(self, X, Y):
        try:
            params = {'reg': X, 'val': int(Y)}
        except ValueError:
            params = {'reg': X, 'val': self.get_register(Y)}
        return params

    def recover_last_sound(self, reg):
        if reg.isdigit():
            reg = int(reg)
        else:
            reg = self.get_register(reg)
        
        if reg != 0:
            return self.last_sound
        else:
            return None

    def jump_instructions(self, test_val, offset):
        if test_val > 0:
            return offset
        else:
            return 1

    def parse_instruction(self, instruction):

        parts = instruction.split()

        if parts[0] == 'set':
            func = self.set_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'snd':
            func = self.play_sound
            params = {'reg': parts[1]}

        elif parts[0] == 'add':
            func = self.add_to_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'mul':
            func = self.multiply_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'mod':
            func = self.modulo_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'rcv':
            func = self.recover_last_sound
            params = {'reg': parts[1]}
            
        elif parts[0] == 'jgz':
            func = self.jump_instructions

            try:
                test_val = int(parts[1])
            except ValueError:
                test_val = self.get_register(parts[1])

            try:
                offset = int(parts[2])
            except ValueError:
                offset = self.get_register(parts[2])

            params = {'test_val': test_val, 'offset': offset}

        else:
            raise ValueError('Unrecognized instruction')
    
        return func, params
    
    def execute_program(self, program, return_first=True):

        if isinstance(program, str):
            program = program.replace('\r', '').split('\n')
        
        current_instruction = 0
        last_recovered_sound = None

        while current_instruction >= 0 and current_instruction < len(program):
            func, params = self.parse_instruction(program[current_instruction])
            
            res = func(**params)

            if func == self.recover_last_sound and res is not None:
                last_recovered_sound = res
                if return_first:
                    break
            
            if func == self.jump_instructions:
                current_instruction += res
            else:
                current_instruction += 1
        
        return last_recovered_sound


class Program(SoundCard):
    def __init__(self, id):
        super(Program, self).__init__()

        self.id = id
        self.other_program = None
        self.set_register('p', self.id)
        self.queue = Queue()
        self.values_sent = 0
        self.waiting = False

    async def send(self, reg):
        if reg.isdigit():
            val = int(reg)
        else:
            val = self.get_register(reg)

        self.other_program.queue.put_nowait(val)

        self.values_sent += 1

    async def receive(self, reg):
        self.waiting = True
        while True:
            try:
                val = self.queue.get_nowait()
                break
            except asyncio.QueueEmpty:
                if self.other_program.queue.empty() and self.other_program.waiting:
                    return
                await asyncio.sleep(1.0)
        self.waiting = False
        self.set_register(reg, val)

    def parse_instruction(self, instruction):

        func, params = super(Program, self).parse_instruction(instruction)

        if func == self.recover_last_sound:
            func = self.receive
        elif func == self.play_sound:
            func = self.send

        return func, params
    
    async def execute_program(self, program):
        if isinstance(program, str):
            program = program.replace('\r', '').split('\n')
        
        current_instruction = 0

        while current_instruction >= 0 and current_instruction < len(program):
            func, params = self.parse_instruction(program[current_instruction])

            if func == self.receive or func == self.send:
                res = await func(**params)
                if self.waiting:
                    break
            else:
                res = func(**params)

            if func == self.jump_instructions:
                current_instruction += res
            else:
                current_instruction += 1

            # print(str(self.id) + ':' + ' '.join(str(r) for r in self.registers[:16]))


TEST_INPUT = '''set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2'''

TEST_INPUT2 = '''snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d'''

with open('data/day18_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':
    sound_card = SoundCard()

    assert sound_card.execute_program(TEST_INPUT) == 4
    
    prog0 = Program(0)
    prog1 = Program(1)
    prog1.other_program = prog0
    prog0.other_program = prog1

    futures = [prog0.execute_program(TEST_INPUT2), prog1.execute_program(TEST_INPUT2)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))

    assert prog1.values_sent == 3

    print('All tests passed!')
    sound_card = SoundCard()
    print('Solution 1: {:}'.format(sound_card.execute_program(PUZZLE_INPUT)))

    prog0 = Program(0)
    prog1 = Program(1)
    prog1.other_program = prog0
    prog0.other_program = prog1

    futures = [prog0.execute_program(PUZZLE_INPUT), prog1.execute_program(PUZZLE_INPUT)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))

    print('Solution 2: {:}'.format(prog1.values_sent))