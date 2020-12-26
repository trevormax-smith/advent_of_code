# Advent of Code 2015, Day 6
# Michael Bell
# 12/26/2020

import helper

def parse_instruction(instruction):
    instruction_parts = instruction.replace('through ', '').replace('turn ', '').split(' ')

    action = instruction_parts[0]
    tlc = tuple([int(c) for c in instruction_parts[1].split(',')])
    brc = tuple([int(c) for c in instruction_parts[2].split(',')])

    return action, tlc, brc


def new_lighting_array():
    lighting_array = [[0] * 1000 for _ in range(1000)]
    return lighting_array


class BinaryLightingArray(object):
    def __init__(self):
        self.lighting_array = new_lighting_array()
    
    def set_lights(self, instructions):
        for instruction in instructions:
            action, tlc, brc = parse_instruction(instruction)

            for row in range(tlc[0], brc[0]+1):
                for col in range(tlc[1], brc[1]+1):
                    getattr(self, action)(row, col)
    
    def on(self, row, col):
        self.lighting_array[row][col] = 1
    def off(self, row, col):
        self.lighting_array[row][col] = 0
    def toggle(self, row, col):
        self.lighting_array[row][col] = (self.lighting_array[row][col] + 1) % 2
    
    def total_brightness(self):
        return sum(light for row in self.lighting_array for light in row)


class LightingArray(BinaryLightingArray):
    def on(self, row, col):
        self.lighting_array[row][col] = self.lighting_array[row][col] + 1
    def off(self, row, col):
        self.lighting_array[row][col] = max([self.lighting_array[row][col] - 1, 0])
    def toggle(self, row, col):
        self.lighting_array[row][col] = self.lighting_array[row][col] + 2


assert parse_instruction('turn on 489,959 through 759,964') == ('on', (489, 959), (759, 964))
assert parse_instruction('turn off 820,516 through 871,914') == ('off', (820, 516), (871, 914))
assert parse_instruction('toggle 275,796 through 493,971') == ('toggle', (275, 796), (493, 971))

instructions = helper.read_input_lines(6)
lighting_array = BinaryLightingArray()
lighting_array.set_lights(instructions)
print('Part 1:', lighting_array.total_brightness())

lighting_array = LightingArray()
lighting_array.set_lights(instructions)
print('Part 2:', lighting_array.total_brightness())
