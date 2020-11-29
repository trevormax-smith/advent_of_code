# Code for the 2018 AoC, day 2
# https://adventofcode.com/2018/day/2
# Michael Bell
# 12/2/2018
from sortedcontainers import SortedList
from time import time


def has_n_of_any_char(box_id, n=2):
    """
    Test whether the given string BOX_ID contains exactly N occurrances of any character. 
    Returns True if a repeated character is found, False otherwise.
    
    Example:
        The input 'aabcd' would return True if n=2, False if n=3.
    """
    unique_chars = set(box_id)

    for uc in unique_chars:
        if box_id.count(uc) == n:
            return True
    return False


def checksum(box_ids):
    """
    For a given list of strings, return a checksum that is the product of the number of strings that
    have 2 of the same characters times the number of strings with 3 of the same characters.
    """
    ids_w_n = lambda x: sum(
        1 if has_n_of_any_char(box_id, n=x) else 0 for box_id in box_ids
    )

    n_w_2 = ids_w_n(2)
    n_w_3 = ids_w_n(3)

    return n_w_2 * n_w_3


def find_neighboring_ids(box_ids):
    """
    Search through a list of strings of identical length to find two that have the same
    characters apart from one in the same position in each string. Returns the set of common 
    characters or None if no matching pair is found.
    """

    id_len = len(box_ids[0])

    for i in range(id_len):
        ko_ids = SortedList([box_id[:i] + box_id[(i+1):] for box_id in box_ids])

        for box_id1, box_id2 in zip(ko_ids[:-1], ko_ids[1:]):
            if box_id1 == box_id2:
                return box_id1

    return None


def find_neighboring_ids_slow(box_ids):
    """
    A slower implementation of the above using loops.
    """
    id_len = len(box_ids[0])

    for i, box_id in enumerate(box_ids):
        for box_id2 in box_ids[:i] + box_ids[(i+1):]:
            for j in range(id_len):
                if (box_id[:j] + box_id[(j+1):]) == (box_id2[:j] + box_id2[(j+1):]):
                    return box_id[:j] + box_id[(j+1):] 
    return None


if __name__ == '__main__':

    test_ids = [
        'abcdef',
        'bababc',
        'abbcde',
        'abcccd',
        'aabcdd',
        'abcdee',
        'ababab'  
    ]

    test_ids2 = [
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'fguij',
        'axcye',
        'wvxyz'
    ]

    assert checksum(test_ids) == 12

    assert find_neighboring_ids(test_ids2) == 'fgij'

    with open('./data/day02_input.txt', 'r') as f:
        input1 = f.readlines()
    
    print(f"Solution 1: {checksum(input1)}")
    
    t0 = time()
    print(f"Solution 2: {find_neighboring_ids(input1)} ({time() - t0} s)")

    t0 = time()
    print(f"Solution 2: {find_neighboring_ids_slow(input1)} ({time() - t0} s)")