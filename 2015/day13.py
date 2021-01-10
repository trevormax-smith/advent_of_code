# Advent of Code 2015, Day 13
# Michael Bell
# 1/10/2021

import itertools
from collections import defaultdict
import helper


def add_me(happiness_ratings):
    people = list(happiness_ratings.keys())

    for person in people:
        happiness_ratings['Me'][person] = 0
        happiness_ratings[person]['Me'] = 0


def parse_puzzle_input(puzzle_input):
    happiness_ratings = defaultdict(dict)
    for line in puzzle_input:
        tokens = line.replace('.', '').split(' ')
        neighbor = tokens[-1]
        person = tokens[0]
        happiness = int(tokens[3])
        sign = 1 if tokens[2] == 'gain' else -1

        happiness_ratings[person][neighbor] = sign * happiness

    return happiness_ratings


def optimal_happiness(happiness_ratings):

    people = list(happiness_ratings.keys())

    highest_score = 0

    for perm in itertools.permutations(people):
        score = 0
        candidate_order = list(perm)
        for l_neighbor, person, r_neighbor in zip([candidate_order[-1]] + candidate_order[:-1], candidate_order, candidate_order[1:] + [candidate_order[0]]):
            score += happiness_ratings[person][l_neighbor] + happiness_ratings[person][r_neighbor]
        if score > highest_score:
            highest_score = score
    
    return highest_score


example_input = '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.'''.split('\n')

example_happiness_ratings = parse_puzzle_input(example_input)
assert optimal_happiness(example_happiness_ratings) == 330

puzzle_input = helper.read_input_lines(13)
happiness_ratings = parse_puzzle_input(puzzle_input)

print('Part 1:', optimal_happiness(happiness_ratings))
add_me(happiness_ratings)
print('Part 2:', optimal_happiness(happiness_ratings))
