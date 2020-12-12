# Advent of Code 2020, Day 12
# Michael Bell
# 12/12/2020
import math
import helper

class Waypoint(object):
    def __init__(self, x, y, ship):
        self.x = x
        self.y = y
        self.ship = ship
    
    def N(self, val):
        self.y += val
    def S(self, val):
        self.y -= val
    def E(self, val):
        self.x += val
    def W(self, val):
        self.x -= val
    def F(self, val):
        for _ in range(val):
            ship.N(self.y)
            ship.E(self.x)
    def R(self, val):
        self.L(-val)
    def L(self, val):
        x = self.x * int(math.cos(math.radians(val))) - self.y * int(math.sin(math.radians(val))) 
        y = self.x * int(math.sin(math.radians(val))) + self.y * int(math.cos(math.radians(val)))
        self.x = x
        self.y = y
        

    def move(self, instruction):
        action = instruction[0]
        value = int(instruction[1:])
        getattr(self, action)(value)
    
    def move_many(self, instructions):
        for instruction in instructions:
            self.move(instruction)


class Ship(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.head = 0  # 0 East, 90 N, 180 W, 270 S
    
    def N(self, val):
        self.y += val
    def S(self, val):
        self.y -= val
    def E(self, val):
        self.x += val
    def W(self, val):
        self.x -= val
    def F(self, val):
        self.x += val * int(math.cos(math.radians(self.head)))
        self.y += val * int(math.sin(math.radians(self.head)))
    def R(self, val):
        self.head -= val
    def L(self, val):
        self.head += val

    def move(self, instruction):
        action = instruction[0]
        value = int(instruction[1:])
        getattr(self, action)(value)
    
    def move_many(self, instructions):
        for instruction in instructions:
            self.move(instruction)

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


# Tests
sample_instructions = '''F10
N3
F7
R90
F11'''.split('\n')

ship = Ship()
ship.move_many(sample_instructions)
assert ship.manhattan_distance() == 25

ship = Ship()
wp = Waypoint(10, 1, ship)
wp.move_many(sample_instructions)
assert ship.manhattan_distance() == 286

# The real thing
instructions = helper.read_input_lines(12)
ship = Ship()
ship.move_many(instructions)
print('Part 1:', ship.manhattan_distance())

ship = Ship()
wp = Waypoint(10, 1, ship)
wp.move_many(instructions)
print('Part 2:', ship.manhattan_distance())
