# Code for the 2017 Advent Of Code, day 4
# http://adventofcode.com/2017
# Michael Bell
# 12/11/2017
# Solutions passed


def passphrase_is_valid(phrase, mode='basic'):

    words = phrase.split()
    if len(words) == len(set(words)):
        if mode == 'basic':
            return True
        elif mode == 'strict':
            for i, word in enumerate(words[:-1]):
                sorted_word = ''.join(sorted(word))
                for j, other_word in enumerate(words[i+1:]):
                    if sorted_word == ''.join(sorted(other_word)):
                        return False
            return True
        else:
            raise ValueError('Invalid mode {:}'.format(mode))
    else:
        return False


def count_valid_passphrases(phrases, validator=None):

    if validator is None:
        validator = passphrase_is_valid

    phrase_list = phrases.split('\n')
    count = 0

    for phrase in phrase_list:
        if not phrase:
            continue
        phrase = phrase.strip()
        if validator(phrase):
            count += 1

    return count


if __name__ == "__main__":

    # TEST
    assert passphrase_is_valid("aa bb cc dd ee")
    assert not passphrase_is_valid("aa bb cc dd aa")
    assert passphrase_is_valid("aa bb cc dd aaa")
    assert passphrase_is_valid("abcde fghij", 'strict')
    assert not passphrase_is_valid("abcde xyz ecdab", 'strict')
    assert passphrase_is_valid("a ab abc abd abf abj", 'strict')
    assert passphrase_is_valid("iiii oiii ooii oooi oooo", 'strict')
    assert not passphrase_is_valid("oiii ioii iioi iiio", 'strict')

    test_phrases = """aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa"""
    assert count_valid_passphrases(test_phrases) == 2

    print("All tests passed!")

    with open('data/day04_input.txt', 'r') as f:
        puzzle_input = f.read()

    strict_validator = lambda x: passphrase_is_valid(x, 'strict')
    print("Solution 1: {:}".format(count_valid_passphrases(puzzle_input)))
    print("Solution 2: {:}".format(count_valid_passphrases(puzzle_input, strict_validator)))
