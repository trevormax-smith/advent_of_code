# Code for the 2018 AoC, day 15
# https://adventofcode.com/2018/day/15
# Michael Bell
# 12/15/2018
from collections import namedtuple
import sys


wall = '#'
open_spot = '.'
elf = 'E'
goblin = 'G'
opponent = {elf: goblin, goblin: elf}
player_types = {elf, goblin}

Position = namedtuple('Position', 'x, y')


class Player(object):
    def __init__(self, team, x, y, health=200):
        self.health = health
        self.power = 3
        self.x, self.y = x, y
        assert team in player_types
        self.team = team
    
    def map_repr(self):
        return self.team
    
    def __repr__(self):
        return f'Player({self.team}, {self.x}, {self.y}, health={self.health})'
   

def parse_map(text_map):

    map_lines = text_map.split('\n')
   
    field = []
    players = [] 

    for y, row in enumerate(map_lines):
        field_line = str(row)
        for x, square in enumerate(row):
            if square == 'E':
                players.append(Player('E', x, y))
                field_line = field_line.replace('E', '.', 1)
            elif square == 'G':
                players.append(Player('G', x, y))
                field_line = field_line.replace('G', '.', 1)

        field.append(field_line)

    return field, players


def print_field_and_players(field, players):
    for y, line in enumerate(field):
        these_players = [player for player in players if player.y == y]

        to_print = str(line)
        for player in these_players:
            to_print = to_print[:player.x] + player.map_repr() + to_print[(player.x + 1):]

        print(to_print)


def dijkstras_alg(source, dest, field, players):
    dist_grid = []

    active = source
    unvisited = []
    visited = [active]

    for y, row in enumerate(field):
        dist_row = []
        for x, cell in enumerate(row):
            if any(player.x == x and player.y == y for player in players) or cell == wall:
                dist_row.append(None)
            elif source.x == x and source.y == y:
                dist_row.append(0)
            else:
                dist_row.append(sys.maxsize)
        



if __name__ == '__main__':


    test_map = '''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######'''

    field, players = parse_map(test_map)
