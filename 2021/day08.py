from typing import List, Tuple, Dict
from helper import read_input_lines


def parse_input(input_list: List[str]) -> Tuple[List[List[str]], List[List[str]]]:
    signal_patterns = []
    output_values = []
    for line in input_list:
        signal_pattern, output_value = line.split(' | ')
        signal_patterns.append(
            signal_pattern.split()
        )
        output_values.append(
            output_value.split()
        )
    return signal_patterns, output_values


def count_unique_digits(output_values: List[List[str]]) -> int:
    count = 0
    for these_output_values in output_values:
        count += sum(1 for ov in these_output_values if len(ov) in [2, 3, 4, 7])
    return count


def pick_a_pattern(signal_patterns: List[str], digit_count: int) -> List[str]:
    return [p for p in signal_patterns if len(p) == digit_count]


def sort_str(s: str) -> str:
    return ''.join(sorted(s))


def deduce_pattern(signal_patterns: List[str]) -> Dict[str, int]:
    pattern_map = {}

    pick = lambda x: pick_a_pattern(signal_patterns, x)

    pattern_map[1] = pick(2)[0]
    pattern_map[4] = pick(4)[0]
    pattern_map[7] = pick(3)[0]
    pattern_map[8] = pick(7)[0]

    five_digit_patterns = pick(5)
    six_digit_patterns = pick(6)

    # 3 is the 5 digit pattern that contains both of ones digits
    pattern_map[3] = [dp for dp in five_digit_patterns if all(pmd in dp for pmd in pattern_map[1])][0]
    five_digit_patterns.remove(pattern_map[3])
    
    # 9 is the 6 digit pattern that contains all of the digits of 3
    pattern_map[9] = [dp for dp in six_digit_patterns if all(pmd in dp for pmd in pattern_map[3])][0]
    six_digit_patterns.remove(pattern_map[9])

    # 5 is the remaining five digit pattern that is a subset of the 9
    pattern_map[5] = [dp for dp in five_digit_patterns if all(d in pattern_map[9] for d in dp)][0]
    five_digit_patterns.remove(pattern_map[5])

    # 2 is the only remaining five digit pattern
    pattern_map[2] = five_digit_patterns[0]

    # 6 is the 6 digit pattern that contains the segments of 5
    pattern_map[6] = [dp for dp in six_digit_patterns if all(pmd in dp for pmd in pattern_map[5])][0]
    six_digit_patterns.remove(pattern_map[6])

    # zero is the only remaining digit
    pattern_map[0] = six_digit_patterns[0]

    return {sort_str(pattern_map[k]): k for k in pattern_map}


def decode_output(output_values: List[str], pattern_map: Dict[str, int]) -> int:
    output_number = 0
    for i, v in enumerate(output_values[::-1]):
        output_number += 10 ** i * pattern_map[sort_str(v)]
    return output_number


def sum_output(signal_patterns: List[List[str]], output_values: List[List[str]]) -> int:

    output_sum = 0

    for these_signal_patterns, these_output_values in zip(signal_patterns, output_values):

        digit_pattern = deduce_pattern(these_signal_patterns)
        output_sum += decode_output(these_output_values, digit_pattern)

    return output_sum


### TEST
small_test_input = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf']
small_test_signal_patterns, small_test_output_values = parse_input(small_test_input)
small_test_pattern = deduce_pattern(small_test_signal_patterns[0])
small_test_output = decode_output(small_test_output_values[0], small_test_pattern)
assert small_test_output == 5353

test_input = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''.split('\n')

test_signal_patterns, test_output_values = parse_input(test_input)
assert count_unique_digits(test_output_values) == 26
assert sum_output(test_signal_patterns, test_output_values) == 61229

### THE REAL THING
input_lines = read_input_lines(8)
signal_patterns, output_values = parse_input(input_lines)
print(f'Part 1: {count_unique_digits(output_values)}')
print(f'Part 2: {sum_output(signal_patterns, output_values)}')
