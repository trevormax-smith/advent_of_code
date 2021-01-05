# Advent of Code 2015, Day 9
# Michael Bell
# 1/5/2021
from itertools import permutations
import helper


def parse_distances(distances):
    cities = []
    p2p_distances = {}

    for dist in distances:
        c, d = dist.split(' = ')
        d = int(d)
        c1, c2 = c.split(' to ')

        cities.extend([c1, c2])
        p2p_distances[tuple(sorted([c1, c2]))] = d
    
    return set(cities), p2p_distances


def get_ext_dist(cities, p2p_distances, ext='min'):
    if ext == 'min':
        ext_dist = sum(p2p_distances[k] for k in p2p_distances)
    else:
        ext_dist = -1

    for candidate_city_list in permutations(cities, len(cities)):
        candidate_dist = 0
        for c1, c2 in zip(candidate_city_list[:-1], candidate_city_list[1:]):
            city_pair = tuple(sorted([c1, c2]))
            candidate_dist += p2p_distances[city_pair]
        
        if (ext == 'min' and candidate_dist < ext_dist) or (ext == 'max' and candidate_dist > ext_dist):
            ext_dist = candidate_dist
        
    return ext_dist


example_distances = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''.split('\n')

cities, p2p_distances = parse_distances(example_distances)
assert get_ext_dist(cities, p2p_distances) == 605

distances = helper.read_input_lines(9)
cities, p2p_distances = parse_distances(distances)
print('Part 1:', get_ext_dist(cities, p2p_distances))
print('Part 2:', get_ext_dist(cities, p2p_distances, 'max'))
