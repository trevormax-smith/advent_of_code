"""
Code for the 2017 Advent Of Code, day 14
https://adventofcode.com/2017/day/14
Michael Bell
12/17/2017
Solutions passed
"""

import day10 as knot_hash
import day12 as graph


def hex_char_to_bin(hex_char):
    if hex_char.isdigit():
        int_rep = int(hex_char)
    else:
        alpha_vals = ['a', 'b', 'c', 'd', 'e', 'f']
        int_rep = int(10 + alpha_vals.index(hex_char))
    
    return bin(int_rep).replace('0b', '').zfill(4)


def hex_to_bin(hex_string):
    bin_string = ''
    for char in hex_string:
        bin_string += hex_char_to_bin(char)
    return bin_string


def count_used_squares(key):

    used_square_count = 0

    for i in range(128):
        hash_code = knot_hash.full_knot_hash("{:}-{:}".format(key, str(i)))
        bin_code = hex_to_bin(hash_code)

        used_square_count += sum(1 for square in bin_code if square == '1')
    
    return used_square_count


def cell_to_index(row, col, ncol=128):
    return row * ncol + col


def get_connections(grid):

    node_listings = []
    for row_num, row in enumerate(grid):
        for col_num, val in enumerate(row):
            if val == '1':
                pid = cell_to_index(row_num, col_num)

                connections = []

                if row_num > 0 and grid[row_num - 1][col_num] == '1':
                    connections.append(cell_to_index(row_num - 1, col_num))
                if row_num < len(grid) - 1 and grid[row_num + 1][col_num] == '1':
                    connections.append(cell_to_index(row_num + 1, col_num))
                if col_num > 0 and grid[row_num][col_num - 1] == '1':
                    connections.append(cell_to_index(row_num, col_num - 1))
                if col_num < len(row) - 1 and grid[row_num][col_num + 1] == '1':
                    connections.append(cell_to_index(row_num, col_num + 1))
                
                if len(connections) == 0:
                    connections.append(pid)
            
                node_listings.append(graph.encode_node_listing(pid, connections))

    return '\n'.join(node_listings)


def count_groups(key):
    grid = []

    for i in range(128):
        hash_code = knot_hash.full_knot_hash("{:}-{:}".format(key, str(i)))
        bin_code = hex_to_bin(hash_code)
        grid.append(bin_code)

    node_listings = get_connections(grid)

    node_graph = graph.Graph()
    node_graph.build_graph(node_listings)
        
    return len(node_graph.get_groups())


TEST_INPUT = 'flqrgnkx'
PUZZLE_INPUT = 'hfdlxzhv'

if __name__ == '__main__':
    
    assert count_used_squares(TEST_INPUT) == 8108
    print("All tests passed!")

    print('Solution 1: {:}'.format(count_used_squares(PUZZLE_INPUT)))
    print('Solution 2: {:}'.format(count_groups(PUZZLE_INPUT)))
