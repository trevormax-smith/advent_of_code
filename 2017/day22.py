"""
2017 Advent Of Code, day 22
https://adventofcode.com/2017/day/22
Michael Bell
12/24/2017
Solutions passed
"""


def parse_map(starting_map):
    """
    We will use a sparse rep where we just keep track of which grid cells (coded as row #, col #) 
    are infected.
    """

    infected_cells = set()

    rows = starting_map.replace('\r', '').split('\n')
    
    # Convert from (0, 0) in TLC to the center cell
    col_offset = -(len(rows[0]) // 2)
    row_offset = len(rows[0]) // 2

    for row_num, row in enumerate(rows):

        for col_num, val in enumerate(row):
            if val == '#':
                infected_cells.add((
                    len(row) - 1 - row_num - row_offset, 
                    col_num + col_offset
                ))

    return infected_cells


def turn_right(direction):
    if direction == 'up':
        return 'right'
    elif direction == 'right':
        return 'down'
    elif direction == 'down':
        return 'left'
    else:
        return 'up'


def turn_left(direction):
    if direction == 'up':
        return 'left'
    elif direction == 'right':
        return 'up'
    elif direction == 'down':
        return 'right'
    else:
        return 'down'


def take_step(pos, direction):
    if direction == 'up':
        new_pos = (pos[0] + 1, pos[1])
    elif direction == 'right':
        new_pos = (pos[0], pos[1] + 1)
    elif direction == 'down':
        new_pos = (pos[0] - 1, pos[1])
    else:
        new_pos = (pos[0], pos[1] - 1)
    return new_pos


def count_infections(starting_map, n_bursts):

    carrier_position = (0, 0)
    carrier_direction = 'up'
    infection_count = 0
    infected_cells = parse_map(starting_map)

    for i in range(n_bursts):
        if carrier_position in infected_cells:
            carrier_direction = turn_right(carrier_direction)
            infected_cells.remove(carrier_position)
        else:
            carrier_direction = turn_left(carrier_direction)
            infected_cells.add(carrier_position)
            infection_count += 1

        carrier_position = take_step(carrier_position, carrier_direction)
    
    return infection_count


def count_infections_evolved(starting_map, n_bursts):

    carrier_position = (0, 0)
    carrier_direction = 'up'
    infection_count = 0
    infected_cells = parse_map(starting_map)
    weakened_cells = set()
    flagged_cells = set()

    for i in range(n_bursts):
        if carrier_position in infected_cells:
            carrier_direction = turn_right(carrier_direction)
            infected_cells.remove(carrier_position)
            flagged_cells.add(carrier_position)
        elif carrier_position in weakened_cells:
            weakened_cells.remove(carrier_position)
            infected_cells.add(carrier_position)
            infection_count += 1
        elif carrier_position in flagged_cells:
            # Turn around by turning twice in one direction
            carrier_direction = turn_right(carrier_direction)
            carrier_direction = turn_right(carrier_direction)
            flagged_cells.remove(carrier_position)  # becomes clean
        else:
            carrier_direction = turn_left(carrier_direction)
            weakened_cells.add(carrier_position)

        carrier_position = take_step(carrier_position, carrier_direction)
    
    return infection_count


TEST_INPUT = '''..#
#..
...'''

with open('data/day22_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()

if __name__ == '__main__':

    assert parse_map(TEST_INPUT).difference(set([(1, 1), (0, -1)])) == set()

    assert count_infections(TEST_INPUT, 7) == 5
    assert count_infections(TEST_INPUT, 70) == 41
    assert count_infections(TEST_INPUT, 10000) == 5587
    assert count_infections_evolved(TEST_INPUT, 100) == 26
    assert count_infections_evolved(TEST_INPUT, 10000000) == 2511944
    print('All tests passed!')

    print('Solution 1: {:}'.format(count_infections(PUZZLE_INPUT, 10000)))
    print('Solution 2: {:}'.format(count_infections_evolved(PUZZLE_INPUT, 10000000)))
