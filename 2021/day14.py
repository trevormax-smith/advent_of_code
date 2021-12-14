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


def grow_polymer(polymer: str, rules: List[Dict[str, str]], n_steps: int=10) -> str:
    new_polymer = polymer
    for _ in range(n_steps):
        new_polymer = pair_insertion(new_polymer, rules)
    return new_polymer


def get_element_counts(polymer: str) -> Dict[str, str]:
    element_counts = defaultdict(lambda: 0)
    for e in polymer:
        element_counts[e] += 1
    return element_counts


def max_min_diff(polymer: str) -> int:
    element_counts = get_element_counts(polymer)
    
    return (
        element_counts[max(element_counts, key=lambda x: element_counts[x])] - 
        element_counts[min(element_counts, key=lambda x: element_counts[x])]
    )


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
    assert max_min_diff(new_polymer) == 1588
    new_polymer = grow_polymer(polymer, rules, 40)
    assert max_min_diff(new_polymer) == 2188189693529

    ### THE REAL THING
    puzzle_input = helper.read_input()
    polymer, rules = parse_template_and_rules(puzzle_input)
    new_polymer = grow_polymer(polymer, rules)
    print(f'Part 1: {max_min_diff(new_polymer)}')
    print(f'Part 2: {""}')
