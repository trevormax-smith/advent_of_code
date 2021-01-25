# Advent of Code 2015, Day 18
# Michael Bell
# 1/25/2021

import helper
from itertools import product


ON = '#'
OFF = '.'


def parse_map(light_map):
    rows = []
    for row in light_map:
        this_row = []
        for light in row:
            this_row.append(light)
        rows.append(this_row)
    return rows


neighbor_cells = product([-1, 0, 1], repeat=2)
neighbor_cells = [nc for nc in neighbor_cells if nc != (0, 0)]
def count_neighbors_on(light_map, row_num, col_num):
    neighbors_on = 0
    for d_row, d_col in neighbor_cells:
        neigh_row, neigh_col = row_num + d_row, col_num + d_col
        if 0 <= neigh_row < len(light_map) and 0 <= neigh_col < len(light_map[0]) and light_map[neigh_row][neigh_col] == ON:
            neighbors_on += 1
    return neighbors_on


def update_light_map(light_map, stuck_corners=False):

    corners = get_corner_coords(light_map)

    new_light_map = []
    for row_num, row in enumerate(light_map):
        new_row = []
        for col_num, light_state in enumerate(row):
            
            neighbors_on = count_neighbors_on(light_map, row_num, col_num)

            if stuck_corners and (row_num, col_num) in corners:
                new_row.append(ON)
            elif light_state == ON and neighbors_on not in (2, 3):
                new_row.append(OFF)
            elif light_state == OFF and neighbors_on == 3:
                new_row.append(ON)
            else:
                new_row.append(light_state)

        new_light_map.append(new_row)

    return new_light_map


def count_lights_on(light_map):
    lights_on = 0
    for row in light_map:
        lights_on += sum(1 for light in row if light == ON)
    return lights_on


def update_many(light_map, n_steps, stuck_corners=False):
    updated_map = light_map
    for _ in range(n_steps):
        updated_map = update_light_map(updated_map, stuck_corners)
    return updated_map


def get_corner_coords(light_map):
    return [(0, 0), (len(light_map) - 1, 0), (len(light_map) - 1, len(light_map[0]) - 1), (0, len(light_map[0]) - 1)]


def turn_on_corners(light_map):
    corners = get_corner_coords(light_map)    
    for row_num, col_num in corners:
        light_map[row_num][col_num] = ON


light_map = parse_map(helper.read_input_lines(18))
updated_map = update_many(light_map, 100)
print('Part 1:', count_lights_on(updated_map))

turn_on_corners(light_map)
updated_map = update_many(light_map, 100, True)
print('Part 2:', count_lights_on(updated_map))
