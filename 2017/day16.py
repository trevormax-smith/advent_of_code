"""
Code for the 2017 Advent Of Code, day 16
https://adventofcode.com/2017/day/16
Michael Bell
12/21/2017
Solutions passed
"""


def spin(group, n):
    spun_group = group[:]
    
    spun_group[:n] = group[-n:]
    spun_group[n:] = group[:-n]

    return spun_group


def partner(group, a, b):
    ia = group.index(a)
    ib = group.index(b)
    return exchange(group, ia, ib)


def exchange(group, a, b):
    new_group = group[:]
    new_group[a] = group[b]
    new_group[b] = group[a]
    return new_group


def parse_instruction(instruction):

    if instruction[0] == 's':
        move = spin
        params = {'n': int(instruction[1:])}
    elif instruction[0] == 'x':
        move = exchange
        a, b = instruction[1:].split('/')
        params = {'a': int(a), 'b': int(b)}
    elif instruction[0] == 'p':
        move = partner
        a, b = instruction[1:].split('/')
        params = {'a': a, 'b': b}

    return move, params


def dance(instructions, group=None):
    if isinstance(instructions, str):
        instructions = instructions.strip().split(',')
    
    if group is None:
        group = [val for val in 'abcdefghijklmnop']
    else:
        group = [val for val in group]

    for instruction in instructions:

        move, params = parse_instruction(instruction)

        group = move(group, **params)

    return ''.join(group)


def keep_dancing(instructions, N, group=None):
    if isinstance(instructions, str):
        instructions = instructions.strip().split(',')

    if group is None:
        group = 'abcdefghijklmnop'

    # Find the unique set of configurations and how long until we cycle back to the start
    group_configs = [group]
    for i in range(0, N):
        group = dance(instructions, group)
        if group in group_configs:
            break
        group_configs.append(group)
        if (i+1) % 10000000 == 0:
            print(i+1)

    # Then we figure out where we would be in the loop at the requested number of iterations
    ndx = N % len(group_configs) if len(group_configs) < N else i + 1

    return group_configs[ndx]


with open('data/day16_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':

    assert spin(['a', 'b', 'c', 'd', 'e'], 3) == ['c','d', 'e', 'a', 'b']
    assert spin(['a', 'b', 'c', 'd', 'e'], 1) == ['e', 'a', 'b', 'c', 'd']
    assert parse_instruction('s3') == (spin, {'n': 3})
    assert exchange(['e','a','b','c','d'], 3, 4) == ['e', 'a', 'b', 'd', 'c']
    assert partner(['e','a','b','d','c'], 'e', 'b') == ['b','a','e','d','c']

    assert dance('s1,x3/4,pe/b', 'abcde') == 'baedc'
    assert keep_dancing('s1,x3/4,pe/b', 2, 'abcde') == 'ceadb'

    print('All tests passed!')
    print('Solution 1: {:}'.format(dance(PUZZLE_INPUT)))
    print('Solution 2: {:}'.format(keep_dancing(PUZZLE_INPUT, 1000000000)))
