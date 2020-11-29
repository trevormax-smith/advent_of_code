# Code for the 2018 AoC, day 1
# https://adventofcode.com/2018/day/1
# Michael Bell
# 12/1/2018
import itertools
from time import time
from sortedcontainers import SortedList


def frequency_drift(freq_changes, start_freq=0):

    return start_freq + sum(freq_changes)


def first_repeated_frequency(freq_changes, start_freq=0):
    """
    This is pretty inefficient. Any better way?
    """
    freqs = []
    current_freq = start_freq
    for fc in itertools.chain.from_iterable(itertools.repeat(freq_changes)):
        if current_freq not in freqs:
            freqs.append(current_freq)
        else:
            break
        current_freq += fc

    return current_freq    


def first_repeated_frequency_faster(freq_changes, start_freq=0):
    """
    This is pretty inefficient. Any better way?
    """
    freqs = SortedList()
    current_freq = start_freq
    for fc in itertools.chain.from_iterable(itertools.repeat(freq_changes)):
        if current_freq not in freqs:
            freqs.add(current_freq)
        else:
            break
        current_freq += fc

    return current_freq


def parse_freq_changes(freq_changes_file):
    with open(freq_changes_file, 'r') as f:
        fcs = f.readlines()

    return [int(i) for i in fcs]


if __name__ == '__main__':

    test1 = [1, -2, 3, 1]
    test2 = [1, 1, 1]
    test3 = [1, 1, -2]
    test4 = [-1, -2, -3]

    assert frequency_drift(test1) == 3
    assert frequency_drift(test2) == 3
    assert frequency_drift(test3) == 0
    assert frequency_drift(test4) == -6

    assert first_repeated_frequency(test1) == 2

    input1 = parse_freq_changes('./data/day01_input.txt')

    print(f'Solution 1: {frequency_drift(input1)}')

    t0 = time()
    print(f'Solution 2: {first_repeated_frequency_faster(input1)} ({time() - t0} s)')
    t0 = time()
    print(f'Solution 2: {first_repeated_frequency(input1)} ({time() - t0} s)')
    