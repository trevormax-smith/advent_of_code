# Advent of Code 2015, Day 12
# Michael Bell
# 1/9/2021

import helper
import json


def add_numbers(obj, ignore_red=False):
    sum_of_numbers = 0

    if ignore_red and isinstance(obj, dict) and 'red' in obj.values():
        return 0

    for entry in obj:
        if isinstance(entry, list) or isinstance(entry, dict):
            sum_of_numbers += add_numbers(entry, ignore_red)
        elif isinstance(obj, dict) and (isinstance(obj[entry], list) or isinstance(obj[entry], dict)):
            sum_of_numbers += add_numbers(obj[entry], ignore_red)
        elif (isinstance(obj, dict) and not isinstance(obj[entry], str)):
            sum_of_numbers += obj[entry]
        elif not isinstance(entry, str):
            sum_of_numbers += entry

    return sum_of_numbers

test = json.loads('[1,{"c":"red","b":2},3]')
assert add_numbers(test) == 6
assert add_numbers(test, True) == 4

puzzle_input = json.loads(helper.read_input(12))

print("Part 1:", add_numbers(puzzle_input))
print("Part 2:", add_numbers(puzzle_input, True))
