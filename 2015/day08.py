# Advent of Code 2015, Day 8
# Michael Bell
# 1/4/2021

import helper


def characters_in_code(lines):
    return sum(len(line) for line in lines)


def characters_in_memory(lines):
    n_chars = 0
    for line in lines:
        a = line.replace(r'\\', ' ').replace(r'\"', ' ')[1:-1]

        while r'\x' in a:
            i = a.index(r'\x')
            a = a[:i] + ' ' + a[i+4:]

        n_chars += len(a)

    return n_chars


def characters_newly_encoded(lines):

    n_chars = 0
    for line in lines:
        a = '"' + line.replace('\\', r'\\').replace(r'"', r'\"') + '"'

        n_chars += len(a)

    return n_chars


example_file = r'''""
"abc"
"aaa\"aaa"
"\x27"'''.split('\n')

assert characters_in_code(example_file) == 23
assert characters_in_memory(example_file) == 11

real_file = helper.read_input_lines(8)

print('Part 1:', characters_in_code(real_file) - characters_in_memory(real_file))
print('Part 2:', characters_newly_encoded(real_file) - characters_in_code(real_file))
