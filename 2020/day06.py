# Advent of Code 2020, Day 6
# Michael Bell
# 12/6/2020
from collections import defaultdict, namedtuple
from typing import List

import helper


group_declaration = namedtuple('GroupDeclaration', 'size, declarations')


def parse_group_declaration(group_decs: str) -> group_declaration:

    q_to_people = defaultdict(list)  # Indexed on the question ID, a list of people IDs in the group that answered yes
    ind_decs = [ind_dec for ind_dec in group_decs.split('\n') if ind_dec.strip()]
    group_size = len(ind_decs)

    for person_id, ind_dec in enumerate(ind_decs):
        for q in ind_dec:
            q_to_people[q].append(person_id)
    
    return group_declaration(group_size, q_to_people)


def parse_declaration_batch(all_decs: str) -> List[group_declaration]:
    decs = all_decs.split('\n\n')
    group_decs = [parse_group_declaration(group_dec) for group_dec in decs]
    return group_decs


def count_qs(group_decs: List[group_declaration]) -> int:
    return sum(len(group.declarations) for group in group_decs)


def count_unanimous_qs(group_decs: List[group_declaration]) -> int:
    return sum(1 for group in group_decs for q in group.declarations if len(group.declarations[q]) == group.size)


sample_declaration_batch = '''abc

a
b
c

ab
ac

a
a
a
a

b'''
sample_declarations = parse_declaration_batch(sample_declaration_batch)
assert count_qs(sample_declarations) == 11
assert count_unanimous_qs(sample_declarations) == 6

declarations_batch = helper.read_input(6)
declarations = parse_declaration_batch(declarations_batch)
print("Part 1:", count_qs(declarations))
print("Part 2:", count_unanimous_qs(declarations))
