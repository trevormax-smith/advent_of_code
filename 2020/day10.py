# Advent of Code 2020, Day 10
# Michael Bell
# 12/10/2020
from itertools import combinations
import helper

# For part 2:
#   Wherever there is a diff of 3, those points in the chain are fixed (adapters on either side of the break)
#   Between the diffs of 3, count possible combos of sub-chains
#   Total configs is product of sub-chain possibilities
# 
#   A block of 2... it has 1
#       e.g. 1, 2 can only be 12
#   What about a block of 3... it has 2
#       e.g. 1, 2, 3 can have 123, 13
#   Every block of 4 contiguous has 4 configs
#       e.g. 1, 2, 3, 4 can have 1234, 124, 134, 14
#   What about a block of 5... it has 8
#       e.g. 1, 2, 3, 4, 5... 1234 5, 124 5, 134 5, 14 5, 1 2345 (already got it), 1 235, 1 245, 1 25, 135
#   Is the number of combos for N adapters spaced 1 apart, where ends are fixed, 2 ** (N - 2)


def get_possible_chains(sub_chain):
    if len(sub_chain) <= 2:
        return 1

    start = sub_chain[0]
    end = sub_chain[-1]
    to_reshuffle = sub_chain[1:-1]

    min_combos = len(to_reshuffle) // 3
    max_combos = len(to_reshuffle)

    n_combos = 0

    for r in range(min_combos, max_combos + 1):
        for c in combinations(to_reshuffle, r):
            candidate_chain = sorted([start] + list(c) + [end])
            candidate_diffs = adapter_chain_differences(candidate_chain)
            if all(cd <= 3 for cd in candidate_diffs):
                n_combos += 1
    
    return n_combos


def parse_adapter_list(adapter_list):
    return [int(a) for a in adapter_list]


def chain_adapters(adapter_list):
    return sorted([0] + adapter_list + [max(adapter_list) + 3])


def adapter_chain_differences(adapter_chain):
    return [b - a for a, b in zip(adapter_chain[:-1], adapter_chain[1:])]


def count_configs(adapter_list):
    adapter_chain = chain_adapters(adapter_list)
    diffs = adapter_chain_differences(adapter_chain)
    # Probably fucking up the indexing here... need to think about it more
    # My logic should work for first example
    sub_chain_combos = []
    chain_start = 0
    for i, diff in enumerate(diffs):
        if diff == 3:
            chain_end = i
            this_combos = max((2 ** (chain_end - chain_start + 1 - 2), 1))
            sub_chain_combos.append(this_combos)
            chain_start = i + 1

    combos = 1
    for combo in sub_chain_combos:
        combos *= combo
    return combos


def count_configs2(adapter_list):
    adapter_chain = chain_adapters(adapter_list)
    chain_len = len(adapter_chain)
    chain_start = 0
    chain_end = 1

    combos = 1

    while chain_end < chain_len:
        if adapter_chain[chain_end] - adapter_chain[chain_end - 1] == 3:
            # 0 3 4 5 8 9 12
            sub_chain = adapter_chain[chain_start:chain_end]
            n_combos = get_possible_chains(sub_chain)
            combos *= n_combos
            chain_start = chain_end
        chain_end += 1

    return combos

def part1_answer(adapter_chain_differences):
    n_diffs = len(adapter_chain_differences)
    n_1_diffs = sum(1 for d in adapter_chain_differences if d == 1)
    n_2_diffs = sum(1 for d in adapter_chain_differences if d == 2)
    n_3_diffs = sum(1 for d in adapter_chain_differences if d == 3)
    print(n_diffs, n_1_diffs, n_2_diffs, n_3_diffs)
    assert n_diffs == n_1_diffs + n_3_diffs + n_2_diffs
    return n_1_diffs * n_3_diffs


sample_adapters = '''16
10
15
5
1
11
7
19
6
12
4'''.split('\n')
sample_adapters = parse_adapter_list(sample_adapters)
sample_adapter_chain = chain_adapters(sample_adapters)
sample_diffs = adapter_chain_differences(sample_adapter_chain)
assert part1_answer(sample_diffs) == 35
print(count_configs(sample_adapters))
print(count_configs2(sample_adapters))
assert count_configs(sample_adapters) == 8


sample_adapters = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''.split('\n')
sample_adapters = parse_adapter_list(sample_adapters)
sample_adapter_chain = chain_adapters(sample_adapters)
sample_diffs = adapter_chain_differences(sample_adapter_chain)
assert part1_answer(sample_diffs) == 220
assert count_configs2(sample_adapters) == 19208

adapters = parse_adapter_list(helper.read_input_lines(10))
adapter_chain = chain_adapters(adapters)
diffs = adapter_chain_differences(adapter_chain)
print("Part 1:", part1_answer(diffs))
print("Part 2:", count_configs2(adapters))
