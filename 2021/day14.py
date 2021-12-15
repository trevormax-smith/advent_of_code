from collections import defaultdict
from typing import List, Tuple, Dict
import helper


def parse_template_and_rules(puzzle_input: str) -> Tuple[str, List[Dict[str, str]]]:
    template, the_rules = puzzle_input.strip().split('\n\n')
    rules = {}
    for the_rule in the_rules.split('\n'):
        pair, replacement = the_rule.split(' -> ')
        rules[pair] = replacement
    return template, rules


def pair_insertion(polymer: str, rules: List[Dict[str, str]]) -> str:
    input_position = 0
    output_position = 1
    new_polymer = str(polymer)

    while input_position < (len(polymer) - 1):
        pair = polymer[input_position:input_position+2]
        to_insert = rules[pair]
        new_polymer = new_polymer[:output_position] + to_insert + new_polymer[output_position:]
        input_position += 1
        output_position += 2
    
    return new_polymer


def faster_grow_polymer(polymer: str, rules: List[Dict[str, str]], n_steps: int=10) -> int:
    
    element_counts = get_element_counts(polymer)
    pair_counts = get_pair_counts(polymer)

    for _ in range(n_steps):
        next_pair_counts = pair_counts.copy()

        for pair in pair_counts:
            inserted_element = rules[pair]
            element_counts[inserted_element] += pair_counts[pair]

            new_pair1 = f'{pair[0]}{inserted_element}'
            new_pair2 = f'{inserted_element}{pair[1]}'
            next_pair_counts[pair] -= pair_counts[pair]
            next_pair_counts[new_pair1] += pair_counts[pair]
            next_pair_counts[new_pair2] += pair_counts[pair]

        pair_counts = next_pair_counts.copy()
    
    return max_min_diff(element_counts)


def grow_polymer(polymer: str, rules: List[Dict[str, str]], n_steps: int=10) -> str:
    new_polymer = polymer
    for _ in range(n_steps):
        new_polymer = pair_insertion(new_polymer, rules)
    return new_polymer


def get_element_counts(polymer: str) -> Dict[str, int]:
    element_counts = defaultdict(lambda: 0)
    for e in polymer:
        element_counts[e] += 1
    return element_counts


def get_pair_counts(polymer:str) -> Dict[str, int]:
    pair_counts = defaultdict(lambda: 0)
    for e1, e2 in zip(polymer[:-1], polymer[1:]):
        pair_counts[f'{e1}{e2}'] += 1
    return pair_counts


def max_min_diff(element_counts: Dict[str, int]) -> int:
    return max(element_counts.values()) - min(element_counts.values())


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''

    polymer, rules = parse_template_and_rules(test_input)
    new_polymer = pair_insertion(polymer, rules)
    print(f"Template:     {polymer}")
    print(f"After step 1: {new_polymer}")
    new_polymer = pair_insertion(new_polymer, rules)
    print(f"After step 2: {new_polymer}")
    new_polymer = pair_insertion(new_polymer, rules)
    print(f"After step 3: {new_polymer}")
    new_polymer = pair_insertion(new_polymer, rules)
    print(f"After step 4: {new_polymer}")

    new_polymer = grow_polymer(polymer, rules)
    element_counts = get_element_counts(new_polymer)
    assert max_min_diff(element_counts) == 1588
    assert faster_grow_polymer(polymer, rules) == 1588
    assert faster_grow_polymer(polymer, rules, 40) == 2188189693529

    ### THE REAL THING
    puzzle_input = helper.read_input()
    polymer, rules = parse_template_and_rules(puzzle_input)
    new_polymer = grow_polymer(polymer, rules)
    element_counts = get_element_counts(new_polymer)
    print(f'Part 1: {max_min_diff(element_counts)}')
    print(f'Part 2: {faster_grow_polymer(polymer, rules, 40)}')
