# Advent of Code 2015, Day 17
# Michael Bell
# 1/16/2021

import helper
from itertools import combinations


def get_combos(volume, containers, min_number=False):

    n = len(containers)

    sorted_containers = sorted(containers)
    for i in range(1, n+1):
        cont_vol = sum(sorted_containers[:i])
        if cont_vol == volume:
            longest_combo = i
        elif cont_vol > volume:
            longest_combo = i - 1
        else:
            continue
        break

    sorted_containers = [sc for sc in sorted_containers[::-1]]
    for i in range(1, n+1):
        cont_vol = sum(sorted_containers[:i])
        if cont_vol >= volume:
            shortest_combo = i
        else:
            continue
        break
    
    if min_number:
        longest_combo = shortest_combo

    combos = []
    for combo_len in range(shortest_combo, longest_combo+1):
        for combo in combinations(containers, combo_len):
            if sum(combo) == volume:
                combos.append(combo)
    
    return combos


test_containers = [20, 15, 10, 5, 5]
assert len(get_combos(25, test_containers)) == 4

containers = [int(c) for c in helper.read_input_lines(17)]
print('Part 1:', len(get_combos(150, containers)))
print('Part 2:', len(get_combos(150, containers, True)))
