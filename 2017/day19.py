"""
2017 Advent Of Code, day 19
https://adventofcode.com/2017/day/19
Michael Bell
12/23/2017
Solutions passed!
"""
from typing import List, Tuple


def parse_maze(maze_as_string: str) -> List[List[str]]:
    grid_lines = maze_as_string.replace('\r', '').split('\n')

    return [[char for char in line] for line in grid_lines]


TEST_INPUT = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """


def step_in_direction(row: int, col: int, direction: str) -> Tuple:
    
    if direction == 'down':
        row += 1
    elif direction == 'up':
        row -= 1
    elif direction == 'right':
        col += 1
    elif direction == 'left':
        col -= 1
    else:
        raise ValueError(f'Unknown direction {direction}')
    
    return row, col


def get_opposing_direction(direction:str) -> str:
    if direction == 'up':
        return 'down'
    elif direction == 'down':
        return 'up'
    elif direction == 'left':
        return 'right'
    elif direction == 'right':
        return 'left'


def traverse_maze(maze_as_string: str) -> List[str]:

    maze = parse_maze(maze_as_string)

    directions = set(['down', 'up', 'left', 'right'])
    maze_chars = set(['|', '-', '+'])

    breadcrumb: List[str] = []
    row:int = 0
    col:int = maze[row].index('|')
    direction = 'down'
    steps:int = 0

    while True:
        char = maze[row][col]

        if char == ' ':
            break
        elif char not in maze_chars:
            breadcrumb.append(char)
        elif char == '+':
            other_directions = directions.difference(
                [direction, get_opposing_direction(direction)]
            )
            for next_direction in other_directions:
                test_row, test_col = step_in_direction(row, col, next_direction)
                try:
                    if maze[test_row][test_col] != ' ':
                        direction = next_direction
                        break
                except IndexError:
                    pass
        
        row, col = step_in_direction(row, col, direction)
        steps += 1

    return breadcrumb, steps


with open('data/day19_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':
    assert traverse_maze(TEST_INPUT)[0] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert traverse_maze(TEST_INPUT)[1] == 38
    print('Tests passed!')

    print('Solution 1: {:}'.format(''.join(traverse_maze(PUZZLE_INPUT)[0])))
    print('Solution 2: {:}'.format(traverse_maze(PUZZLE_INPUT)[1]))
