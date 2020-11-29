"""
Code for the 2017 Advent Of Code, day 15
https://adventofcode.com/2017/day/15
Michael Bell
12/20/2017
Solutions passed
"""


def num_to_bin(num):

    return bin(num).replace('0b', '').zfill(32)


def bitwise_match(a_val, b_val):

    a_bin = num_to_bin(a_val)
    b_bin = num_to_bin(b_val)

    return a_bin[-16:] == b_bin[-16:]


class Generator(object):

    def __init__(self, factor, starting_value):
        self.value = starting_value
        self.factor = factor
        self.div = 2147483647
        self.counter = 0

    def next_value(self):

        self.value = (self.value * self.factor) % self.div
        self.counter += 1

    def get_valid_values(self, criteria):
        
        while True:
            self.next_value()
            if self.value % criteria == 0:
                yield self.value


def count_valid_matching_pairs(a_init, b_init, N):

    genA = Generator(16807, a_init)
    genB = Generator(48271, b_init)

    n_matches = 0

    for i, (aval, bval) in enumerate(zip(genA.get_valid_values(4), genB.get_valid_values(8))):

        if bitwise_match(aval, bval):
            n_matches += 1

        if (i + 1) % 100000 == 0:
            print(i+1)

        if i >= N:
            break
    
    return n_matches


def count_matching_pairs(a_init, b_init, N):

    genA = Generator(16807, a_init)
    genB = Generator(48271, b_init)

    n_matches = 0

    for i in range(N):
        genA.next_value()
        genB.next_value()

        if bitwise_match(genA.value, genB.value):
            n_matches += 1

        if (i + 1) % 1000000 == 0:
            print(i+1)
    
    return n_matches


if __name__ == '__main__':

    assert count_matching_pairs(65, 8921, 5) == 1
    assert count_valid_matching_pairs(65, 8921, 1056) == 1
    print('Tests passed!')
    print('Solution 1: {:}'.format(count_matching_pairs(722, 354, 40000000)))
    print('Solution 2: {:}'.format(count_valid_matching_pairs(722, 354, 5000000)))
