# Code for the 2018 AoC, day 5
# https://adventofcode.com/2018/day/5
# Michael Bell
# 12/5/2018
import sys


def reduce_polymer(polymer):

    while True:
        pairs_to_remove = []
        for unit1, unit2 in zip(polymer[:-1], polymer[1:]):
            if (
                (unit1.islower() and unit1.upper() == unit2) or 
                (unit1.isupper() and unit1.lower() == unit2)
            ):
                pairs_to_remove.append(unit1 + unit2)
        
        pairs_to_remove = set(pairs_to_remove)
        
        reduced_polymer = polymer
        for unit_pair in pairs_to_remove:
            reduced_polymer = reduced_polymer.replace(unit_pair, '')
        
        if reduced_polymer == '' or reduced_polymer == polymer:
            break
        else:
            polymer = reduced_polymer
    
    return reduced_polymer


def recursive_reduce_polymer(polymer):
    """
    I think this works, but leads to a max recursion error on the full data set.
    """
    for i, unit in enumerate(polymer[:-1]):
        if (
            (unit.islower() and unit.upper() == polymer[i+1]) or 
            (unit.isupper() and unit.lower() == polymer[i+1])
        ):
            return recursive_reduce_polymer(polymer[:i] + polymer[i+2:])
    return polymer


def optimal_polymer_length(polymer):

    units = set(polymer.lower())
    reduced_lengths = {}

    for unit in units:
        reduced_lengths[unit] = len(
            reduce_polymer(
                polymer.replace(unit, '').replace(unit.upper(), '')
            )
        )

    return min(reduced_lengths.values())


if __name__ == '__main__':

    assert reduce_polymer('aA') == ''
    assert reduce_polymer('abBA') == ''
    assert reduce_polymer('abAB') == 'abAB'
    assert reduce_polymer('aabAAB') == 'aabAAB'
    assert reduce_polymer('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'

    with open('./data/day05_input.txt', 'r') as f:
        input1 = f.read()

    print(recursive_reduce_polymer('dabAcCaCBAcCcaDA'))

    reduced_polymer = reduce_polymer(input1)

    print(f'Solution 1: {len(reduced_polymer)}')

    optimal_length = optimal_polymer_length(input1)

    print(f'Solution 2: {optimal_length}')
