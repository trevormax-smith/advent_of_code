# Advent of Code 2015, Day 5
# Michael Bell
# 12/6/2020
import helper


def is_nice(string: str) -> bool:
    verdict = 'ab' not in string and 'cd' not in string and 'pq' not in string and 'xy' not in string

    chars = set(string)
    verdict = verdict and any(c + c in string for c in chars)

    vowels = 'aeiou'
    verdict = verdict and sum(string.count(v) for v in vowels) >= 3

    return verdict


def is_nice_new(string: str) -> bool:

    test2 = False
    test1 = False
    for i, c in enumerate(string[:-2]):
        test2 = test2 or c == string[i+2]
        # Inserting a 0 here so I don't catch false matches from pairs of characters on either side of the pair being tested
        # The last pair is never tested, but it would have already been in the string earlier, so that's OK
        # Actually, I don't really have to test all pairs, just those in the first half of the string... could speed up by oh well
        test1 = test1 or string[i:i+2] in string[:i] + '0' + string[i+2:]
    
    return test1 and test2


assert is_nice('ugknbfddgicrmopn')
assert is_nice('aaa')
assert not is_nice('jchzalrnumimnmhp')
assert not is_nice('haegwjzuvuyypxyu')
assert not is_nice('dvszwmarrgswjxmb')

assert is_nice_new('qjhvhtzxzqqjkmpb')
assert is_nice_new('xxyxx')
assert not is_nice_new('uurcxstgmygtbstg')
assert not is_nice_new('ieodomkazucvgmuy')

string_list = helper.read_input_lines(5)
print("Part 1:", sum(1 for string in string_list if is_nice(string)))
print("Part 2:", sum(1 for string in string_list if is_nice_new(string)))
