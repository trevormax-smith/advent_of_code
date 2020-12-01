# Advent of Code, 2015
# Day 3
# 11/30/2020
from collections import defaultdict


def get_houses_visited(directions):

    current_x, current_y = (0, 0)

    houses_visited = defaultdict(list)

    for i, direction in enumerate(directions):
        houses_visited[(current_x, current_y)].append(i)

        if direction == '>':
            current_x += 1
        elif direction == '<':
            current_x -= 1
        elif direction == '^':
            current_y += 1
        elif direction == 'v':
            current_y -= 1
        else:
            raise ValueError(f"Unexpected direction {direction}")

    return houses_visited


with open('./inputs/day03.txt', 'r') as f:
    directions = f.read()

# Year 1
houses_visited = get_houses_visited(directions)
print(f'Year 1 houses visited at least once: {len(houses_visited)}')

# Year 2
santa_visited_houses = get_houses_visited(directions[::2])
robo_visited_houses = get_houses_visited(directions[1::2])

year_2_house_list = set(
    santa_visited_houses.keys()
).union(set(
    robo_visited_houses.keys()
))

print(f'Year 2 houses visited at least once: {len(year_2_house_list)}')
