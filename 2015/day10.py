# Advent of Code 2015, Day 10
# Michael Bell
# 1/6/2021


def play_game(starting_number, iterations):
    number = starting_number
    for _ in range(iterations):
        new_number = ''
        while len(number) > 0:
            current_digit = number[0]
            n_occurrences = 0
            for dig in number:
                if dig == current_digit:
                    n_occurrences += 1
                else:
                    break
            new_number += f'{n_occurrences}{current_digit}'
            number = number[n_occurrences:]
        number = new_number
    return number


sample_input = '1'
assert play_game(sample_input, 5) == '312211'

puzzle_input = '1113122113'
print('Part 1:', len(play_game(puzzle_input, 40)))
# Didn't do anything to optimize, it just takes a few mins to run
# Might be fun to play with "atomizing" the sequence so it goes faster, as Conway describes
# https://www.youtube.com/watch?v=ea7lJkEhytA
print('Part 2:', len(play_game(puzzle_input, 50)))
