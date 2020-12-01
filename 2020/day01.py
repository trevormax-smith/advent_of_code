# Advent of Code 2020, Day 1
# Michael Bell
# 12/1/2020
from itertools import combinations

def parse_expense_report(expense_report):
    return [int(val) for val in expense_report.split('\n') if val.strip()]


def expense_report_checker(line_items, n_items=2, target_value=2020):

    for items in combinations(line_items, n_items):
        if sum(items) == target_value:
            prod = 1
            for item in items:
                prod *= item
            return prod

    return -1


sample_input = '''1721
979
366
299
675
1456'''

expense_report = parse_expense_report(sample_input)
assert expense_report_checker(expense_report) == 514579
assert expense_report_checker(expense_report, 3) == 241861950

with open('./inputs/day01.txt', 'r') as f:
    expense_report = parse_expense_report(f.read())

print("First solution", expense_report_checker(expense_report))
print("Second solution", expense_report_checker(expense_report, 3))
