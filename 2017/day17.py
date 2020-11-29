"""
2017 Advent Of Code, day 17
https://adventofcode.com/2017/day/17
Michael Bell
12/21/2017
Solutions passed
"""


def spinlock(n_steps, n_cycles=2017, value_after=2017):

    buffer = [0]
    current_position = 0

    for i in range(1, n_cycles + 1):

        current_position = ((current_position + n_steps) % len(buffer)) + 1
        buffer.insert(current_position, i)

        if i % 500000 == 0:
            print(i)

    ndx = buffer.index(value_after) + 1
    if ndx == len(buffer):
        ndx = 0

    return buffer[ndx]


def spinlock_light(n_steps, n_cycles=50000000):

    current_position = 0

    after_zero = None

    for i in range(1, n_cycles + 1):

        current_position = ((current_position + n_steps) % i) + 1

        if current_position == 1:
            after_zero = i
        
        if i % 500000 == 0:
            print(i)
    
    return after_zero


if __name__ == '__main__':

    assert spinlock(3) == 638
    assert spinlock_light(3, 9) == 9

    print('All tests passed!')

    print('Solution 1: {:}'.format(spinlock(337)))
    print('Solution 2: {:}'.format(spinlock_light(337, 50000000)))
