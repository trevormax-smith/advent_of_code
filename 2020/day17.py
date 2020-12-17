# Advent of Code 2020, Day 17
# Michael Bell
# 12/17/2020
from itertools import product
import helper


def relative_neighbor_coords():
    relative_coords = list(product([-1, 0, 1], repeat=3))
    relative_coords.remove((0,0,0))
    return relative_coords

relative_neighbor_coords = relative_neighbor_coords()


def get_neighbor_coords(x, y, z):
    return [(x + nc[0], y + nc[1], z + nc[2]) for nc in relative_neighbor_coords]


def parse_init(init):
    cube = {}
    for y, row in enumerate(init):
        for x, val in enumerate(row):
            if val == '#':
                cube[(x, y, 0)] = 1
    return cube


def fill_empty_neighbors(cube):
    new_cube = cube.copy()
    for coords in cube:
        if cube[coords] == 1:
            neighbor_coords = get_neighbor_coords(*coords)
            for nc in neighbor_coords:
                if nc not in cube:
                    new_cube[nc] = 0
    return new_cube


def count_active_neighbors(cube, coords):
    neighbor_coords = get_neighbor_coords(*coords)
    count = 0
    for nc in neighbor_coords:
        if nc in cube:
            count += cube[nc]
    return count


def cycle_cube(cube, n_cycles):
    
    for _ in range(n_cycles):

        cube = fill_empty_neighbors(cube)
        new_cube = cube.copy()

        for coord in cube:
            an_count = count_active_neighbors(cube, coord)
            if cube[coord] == 1 and (an_count < 2 or an_count > 3):
                new_cube[coord] = 0
            elif cube[coord] == 0 and an_count == 3:
                new_cube[coord] = 1
            
        cube = new_cube.copy()
    
    return cube


sample_init = '''.#.
..#
###'''.split('\n')
cube = parse_init(sample_init)
assert len(cube) == 5
assert cube[(1, 0, 0)] == 1
assert cube[(2, 1, 0)] == 1
assert cube[(0, 2, 0)] == 1
assert cube[(1, 2, 0)] == 1
assert cube[(2, 2, 0)] == 1

cube = cycle_cube(cube, 6)
assert sum(cube[coords] for coords in cube) == 112

init = helper.read_input_lines(17)
cube = parse_init(init)
cube = cycle_cube(cube, 6)
print('Part 1:', sum(cube[coords] for coords in cube))
