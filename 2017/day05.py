# Code for the 2017 Advent Of Code, day 5
# http://adventofcode.com/2017
# Michael Bell
# 12/12/2017
# Solutions passed.

def count_steps_to_exit(puzzle, mode=None):
    """
    Takes a string of numbers separated by spaces as input PUZZLE.
    """
    if mode is None:
        mode = 'simple'

    puzzle = [int(n) for n in puzzle.strip().split()]

    position = 0
    length = len(puzzle)
    steps = 0

    while position < length:

        current_position = position
        position += puzzle[position]
        if mode == 'simple':
            puzzle[current_position] += 1
        elif mode == 'complex':
            if puzzle[current_position] >= 3:
                puzzle[current_position] -= 1
            else:
                puzzle[current_position] += 1
        steps += 1

    return steps

if __name__ == "__main__":

    test_input = """0
3
0
1
-3""".replace('\n', ' ')

    assert count_steps_to_exit(test_input) == 5
    assert count_steps_to_exit(test_input, 'complex') == 10

    print("All tests passed!")

    with open('data/day05_input.txt', 'r') as f:
        puzzle_input = f.read().replace('\n', ' ')

    print("Solution 1: {:}".format(count_steps_to_exit(puzzle_input)))
    print("Solution 2: {:}".format(count_steps_to_exit(puzzle_input, 'complex')))
