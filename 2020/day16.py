# Advent of Code 2020, Day 16
# Michael Bell
# 12/16/2020
from typing import Dict, List, Tuple
import helper


def parse_validation_rules(data: str) -> Dict[str, List[Tuple[int, int]]]:
    validation_rules = {}
    for line in data.split('\n'):
        field_name, range_specs = line.split(': ')
        ranges = []
        for r in range_specs.split(' or '):
            ranges.append(tuple(int(val) for val in r.split('-')))
        validation_rules[field_name] = ranges
    return validation_rules


def parse_tickets(tickets) -> List[List[int]]:
    ticket_data = tickets.split('\n')[1:]
    tickets = []
    for td in ticket_data:
        if td.strip():
            tickets.append([int(val) for val in td.split(',')])
    return tickets


def parse_ticket_data(ticket_data: str) -> Tuple[Dict[str, List[Tuple[int, int]]], List[int], List[List[int]]]:
    validation_rule_data, your_ticket_data, nearby_ticket_data = ticket_data.split('\n\n')

    validation_rules = parse_validation_rules(validation_rule_data)
    your_ticket = parse_tickets(your_ticket_data)[0]
    nearby_tickets = parse_tickets(nearby_ticket_data)

    return validation_rules, your_ticket, nearby_tickets


def validate_tickets(validation_rules: Dict[str, List[Tuple[int, int]]], tix: List[List[int]]) -> Tuple[int, List[List[int]]]:
    '''Returns scanning error rate and a list of valid tickets'''
    scanning_error_rate = 0
    valid_tickets = []

    for ticket in tix:
        is_valid = True
        for val in ticket:
            failed_all = True
            for field in validation_rules:
                range1 = validation_rules[field][0]
                range2 = validation_rules[field][1]
                if test_rule(validation_rules[field], val):
                    failed_all = False
                    break
            if failed_all:
                scanning_error_rate += val
                is_valid = False
        if is_valid:
            valid_tickets.append(ticket)

    return scanning_error_rate, valid_tickets


def product_of_fields(field_order, my_ticket):
    prod = 1
    for field_name, val in zip(field_order, my_ticket):
        if 'departure' in field_name:
            prod *= val
    return prod


def test_rule(rule, val):
    range1 = rule[0]
    range2 = rule[1]
    return range1[0] <= val <= range1[1] or range2[0] <= val <= range2[1]


def find_field_order(rules, tix):
    # Build a set of candidate field names for each column
    # Then I hope one column only has one possible, assign that, remove from other candidates, repeat

    n_cols = len(tix[0])
    n_rows = len(tix)

    candidates = []

    for col in range(n_cols):
        col_candidates = []
        for field_name in rules:
            field_is_possible = True
            for row in range(n_rows):
                if not test_rule(rules[field_name], tix[row][col]):
                    field_is_possible = False
                    break
            if field_is_possible:
                col_candidates.append(field_name)

        candidates.append(col_candidates)
    
    assert all(len(c) > 0 for c in candidates)
    assert any(len(c) == 1 for c in candidates)

    fields_to_determine = set(rules.keys())
    field_assignments = {}
    while len(fields_to_determine) > 0:
        fixed_cols = [i for i, col_candidates in enumerate(candidates) if len(col_candidates) == 1]
        for fix_col in fixed_cols:
            fixed_field = candidates[fix_col][0]
            field_assignments[fix_col] = fixed_field
            fields_to_determine.remove(fixed_field)
            for c in candidates:
                if fixed_field in c:
                    c.remove(fixed_field)

    return [field_assignments[i] for i in range(n_cols)]


### TESTS ##########################################################################
sample_ticket_data = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''

sample_rules, sample_my_tix, sample_tix = parse_ticket_data(sample_ticket_data)
# Test parsing
assert len(sample_my_tix) == 3 and sample_my_tix == [7, 1, 14]
assert 'class' in sample_rules and 'row' in sample_rules and 'seat' in sample_rules
assert sample_rules['class'] == [(1, 3), (5, 7)]
assert len(sample_tix) == 4
assert sample_tix[0] == [7, 3, 47] and sample_tix[-1] == [38, 6, 12]

assert validate_tickets(sample_rules, sample_tix)[0] == 71
assert validate_tickets(sample_rules, sample_tix)[1] == [[7, 3, 47]]

sample_ticket_data = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
'''
sample_rules, sample_my_tix, sample_tix = parse_ticket_data(sample_ticket_data)
_, sample_valid_tix = validate_tickets(sample_rules, sample_tix)
field_order = find_field_order(sample_rules, sample_valid_tix)
assert field_order == ['row', 'class', 'seat']

ticket_data = helper.read_input(16)
rules, my_ticket, tix = parse_ticket_data(ticket_data)
sample_error_rate, valid_tickets = validate_tickets(rules, tix)
print('Part 1:', sample_error_rate)
field_order = find_field_order(rules, valid_tickets)
print('Part 2:', product_of_fields(field_order, my_ticket))
