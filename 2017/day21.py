"""
2017 Advent Of Code, day 21
https://adventofcode.com/2017/day/21
Michael Bell
12/23/2017
Solutions passed!
"""
from math import sqrt


starting_pattern = '.#./..#/###'


def parse_enhancement_rules(enhancement_rule_defs):
    enhancement_rule_defs = enhancement_rule_defs.replace('\r', '').split('\n')

    enhancement_rules = {}

    for rule_def in enhancement_rule_defs:
        from_pattern, to_pattern = rule_def.split(' => ')
        enhancement_rules[from_pattern] = to_pattern
    
    return enhancement_rules

def parse_pattern(pattern_def):
    """
    """

    rows = pattern_def.split('/')
    grid = []
    for row in rows:
        grid.append([char for char in row])

    return grid


def encode_pattern(pattern):
    
    row_strings = [''.join(val for val in row) for row in pattern]
    pattern_def = '/'.join(row for row in row_strings)
    return pattern_def


def rotate_pattern(pattern):
    """
    Rotate a pattern 90 deg CW.
    """

    new_pattern = [row[:] for row in pattern]  # Deep copy of the input pattern

    for row_num, row in enumerate(pattern):
        for col_num, val in enumerate(row):
            new_pattern[col_num][len(row) - row_num - 1] = val

    return new_pattern


def flip_pattern(pattern):
    """
    Flip the given pattern horizontally.
    """

    new_pattern = []

    for row in pattern:
        new_pattern.append([val for val in row[::-1]])

    return new_pattern


def stitch_sub_patterns(sub_patterns):
    
    sub_pattern_size = len(sub_patterns[
        list(sub_patterns.keys())[0]
    ])

    sub_patterns_per_side = int(sqrt(len(sub_patterns)))

    pattern = [
        [0 for i in range(sub_pattern_size * sub_patterns_per_side)] 
        for j in range(sub_pattern_size * sub_patterns_per_side)
    ]

    for sp_coord in sub_patterns:
        base_row = sp_coord[0] * sub_pattern_size
        base_col = sp_coord[1] * sub_pattern_size

        sub_pattern = sub_patterns[sp_coord]

        for row_ndx, row in enumerate(sub_pattern):
            for col_ndx, val in enumerate(row):
                pattern[row_ndx + base_row][col_ndx + base_col] = val

    return pattern


def split_pattern(pattern):
    size = len(pattern)

    sub_patterns = {}

    if size % 2 == 0:
        sub_pattern_size = 2
    elif size % 3 == 0:
        sub_pattern_size = 3
    else:
        raise ValueError(f'Invalid pattern of size {size}')
    
    for row_num, row in enumerate(pattern):
        for col_num, val in enumerate(row):

            sub_row = row_num // sub_pattern_size
            sub_col = col_num // sub_pattern_size

            if (sub_row, sub_col) not in sub_patterns:
                sub_pattern = [
                    [0 for i in range(sub_pattern_size)] for j in range(sub_pattern_size)
                ]
            else:
                sub_pattern = sub_patterns[(sub_row, sub_col)]
            
            sub_pattern[row_num % sub_pattern_size][col_num % sub_pattern_size] = val
            sub_patterns[(sub_row, sub_col)] = sub_pattern
    
    return sub_patterns


def enhance_patterns(sub_patterns, enhancement_rules):

    enhanced_sub_patterns = {}

    for sp_coords in sub_patterns:

        sub_pattern = sub_patterns[sp_coords]

        while True:
            encoded_sp = encode_pattern(sub_pattern)
            if encoded_sp in enhancement_rules:
                enhanced_sub_patterns[sp_coords] = parse_pattern(enhancement_rules[encoded_sp])
                break

            encoded_sp = encode_pattern(flip_pattern(sub_pattern))
            if encoded_sp in enhancement_rules:
                enhanced_sub_patterns[sp_coords] = parse_pattern(enhancement_rules[encoded_sp])
                break

            sub_pattern = rotate_pattern(sub_pattern)
        
        if sp_coords not in enhanced_sub_patterns:
            raise RuntimeError(f'Did not find an enhancement rule for {encoded_sp}')

    return enhanced_sub_patterns


def generate_image(enhancement_rule_defs, niter):

    pattern = parse_pattern(starting_pattern)
    enhancement_rules = parse_enhancement_rules(enhancement_rule_defs)

    for _ in range(niter):
        sub_patterns = split_pattern(pattern)

        sub_patterns = enhance_patterns(sub_patterns, enhancement_rules)

        pattern = stitch_sub_patterns(sub_patterns)

    return pattern


TEST_INPUT = '''../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#'''

TEST_INPUT2 = '''#..#/..../..../#..#'''

with open('data/day21_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == "__main__":

    assert parse_pattern(starting_pattern) == [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]
    assert flip_pattern(parse_pattern(starting_pattern)) == [
        ['.', '#', '.'], 
        ['#', '.', '.'], 
        ['#', '#', '#']
    ]
    assert rotate_pattern(parse_pattern(starting_pattern)) == [
        ['#', '.', '.'], 
        ['#', '.', '#'], 
        ['#', '#', '.']
    ]
    assert encode_pattern([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]) == starting_pattern
    
    sub_patterns = split_pattern(parse_pattern(TEST_INPUT2))
    assert stitch_sub_patterns(sub_patterns) == parse_pattern(TEST_INPUT2)

    pattern = generate_image(TEST_INPUT, 2)
    assert sum(sum(1 for val in row if val == '#') for row in pattern) == 12
    
    print('Tests passed')

    pattern = generate_image(PUZZLE_INPUT, 5)

    print('Solution 1: {:}'.format(sum(sum(1 for val in row if val == '#') for row in pattern)))

    with open('data/day21_outpu1.txt', 'w') as f:
        to_write = '\n'.join([''.join(val for val in row) for row in pattern])
        f.write(to_write)

    pattern = generate_image(PUZZLE_INPUT, 18)

    print('Solution 2: {:}'.format(sum(sum(1 for val in row if val == '#') for row in pattern)))

    with open('data/day21_outpu2.txt', 'w') as f:
        to_write = '\n'.join([''.join(val for val in row) for row in pattern])
        f.write(to_write)

