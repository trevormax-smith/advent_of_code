from typing import Union, List, Tuple
from itertools import combinations  # I wrote my own on day 1, but this is much faster
import helper


def find_first_invalid_number(output: List[int], preamble_length: int=25) -> Union[None, int]:

    out_len = len(output)
    i, j = 0, preamble_length

    while j < out_len:
        current_val = output[j]

        possible_values = [sum(c) for c in combinations(output[i:j], 2)]

        if current_val not in possible_values:
            return current_val

        i += 1
        j += 1

    return None


def find_contiguous_group_that_sums_to(invalid_number: int, output: List[int]) -> Union[int, None]:

    out_len = len(output)

    i = 0
    j = 1

    while i < out_len and output[i] < invalid_number:
        while True:
            sub_list = output[i:j]
            list_sum = sum(sub_list)
            if list_sum == invalid_number:
                return max(sub_list) + min(sub_list)
            elif list_sum > invalid_number:
                break
            j += 1
        i += 1

    return None


def parse_output(output: List[str]) -> List[int]:
    return [int(o) for o in output]


sample_output = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''.split('\n')
sample_output = parse_output(sample_output)
assert find_first_invalid_number(sample_output, 5) == 127
assert find_contiguous_group_that_sums_to(127, sample_output) == 62

output = parse_output(helper.read_input_lines(9))
first_invalid_number = find_first_invalid_number(output)
print('First invalid number:', first_invalid_number)
print('Weakness is:', find_contiguous_group_that_sums_to(first_invalid_number, output))
