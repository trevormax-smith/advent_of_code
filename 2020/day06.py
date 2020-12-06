# Advent of Code 2020, Day 5
# Michael Bell
# 12/6/2020
import helper
from collections import defaultdict


def parse_group_declarations(group_dec):

    dec = defaultdict(list)

    ind_decs = group_dec.split('\n')

    for person_id, ind_dec in enumerate(ind_decs):
        for q in ind_dec:
            dec[q].append(person_id)
    
    return dec


def parse_declaration_batch(all_decs):
    decs = all_decs.split('\n\n')
    group_decs = [parse_group_declarations(group_dec) for group_dec in decs]
    return group_decs


def count_qs(group_decs):
    return sum(len(decs) for decs in group_decs)


def count_unanimous_qs(group_decs):
    unanimous_q_count = 0

    for group_dec in group_decs:

        person_ids = []
        for q in group_dec:
            person_ids.extend(group_dec[q])
        
        n_people = len(set(person_ids))

        unanimous_q_count += sum(1 for q in group_dec if len(group_dec[q]) == n_people)

    return unanimous_q_count
        

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

declarations_batch = helper.read_input(6)
declarations = parse_declaration_batch(declarations_batch)
print("Part 1:", count_qs(declarations))
print("Part 2:", count_unanimous_qs(declarations))
