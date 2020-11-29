"""
Code for the 2017 Advent Of Code, day 10
https://adventofcode.com/2017/day/10
Michael Bell
12/16/2017
Solutions passed
"""


def get_subsequence_circular(seq, start, length):
    """
    Get a subsequence from a list, wrapping around the end of the list as necessary.
    """
    sub_seq = seq[start:start + length]
    if start + length > len(seq):
        sub_seq.extend(seq[:start + length - len(seq)])
    return sub_seq


def set_subsequence_circular(seq, sub_seq, start):
    """
    Set a subset of a list, wrapping around the end of the list as necessary.
    """
    seq_len = len(seq)
    sub_seq_len = len(sub_seq)

    seq[start:start + sub_seq_len] = sub_seq
    if start + sub_seq_len > seq_len:
        seq[:start + sub_seq_len - seq_len] = seq[seq_len:]
    return seq[:seq_len]


class KnotHash(object):
    def __init__(self, elements=256):
        if isinstance(elements, int):
            self.seq = list(range(elements))
        else:
            self.seq = elements
        self.n_elements = len(self.seq)
        self.skip_size = 0
        self.current_position = 0

    def tie_knots(self, lengths):
        """
        Given a list of LENGTHS return the hash code.
        If elements is an integer, construct a list of length ELEMENTS.
        If elements is a list, use that as the list to shuffle.
        """

        for length in lengths:

            if length > self.n_elements:
                raise ValueError(
                    "Lengths cannot be larger than the number of elements {:}!".format(
                        self.n_elements
                    )
                )

            sub_seq = get_subsequence_circular(self.seq, self.current_position, length)
            sub_seq = [val for val in sub_seq[::-1]]
            self.seq = set_subsequence_circular(self.seq, sub_seq, self.current_position)

            self.current_position += length + self.skip_size
            self.current_position = self.current_position % self.n_elements
            self.skip_size += 1

    def check_sequence(self):
        return self.seq[0] * self.seq[1]

    def dense_hash(self):
        dense_hash = []
        for i in range(0, self.n_elements, 16):
            hash_val = 0
            for val in self.seq[i:i+16]:
                hash_val = hash_val ^ val
            dense_hash.append(str(hex(hash_val).replace('0x', '')).zfill(2))
        return ''.join(dense_hash)


def string_to_bytes(input):
    return list(bytes(input, 'ascii'))


def string_to_list(input):
    return [int(val) for val in input.split(',')]


def full_knot_hash(input, niter=64, elements=256):

    lengths = string_to_bytes(input) + EXTRA_LENGTHS

    knots = KnotHash(elements)

    for _ in range(niter):
        knots.tie_knots(lengths)

    return knots.dense_hash()


PUZZLE_INPUTS = "192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12"
EXTRA_LENGTHS = [17, 31, 73, 47, 23]


if __name__ == '__main__':
    # TESTS
    assert get_subsequence_circular([1, 2, 3, 4, 5], 1, 3) == [2, 3, 4]
    assert get_subsequence_circular([1, 2, 3, 4, 5], 3, 3) == [4, 5, 1]
    assert set_subsequence_circular([1, 2, 3, 4, 5], [10, 11, 12], 3) == [12, 2, 3, 10, 11]

    test_knots = KnotHash(5)
    test_knots.tie_knots([3, 4, 1, 5])
    assert test_knots.check_sequence() == 12

    assert string_to_bytes('1,2,3') == [49, 44, 50, 44, 51]

    assert full_knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert full_knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert full_knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert full_knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

    print("All tests passed!")
   
    knots = KnotHash()
    knots.tie_knots(string_to_list(PUZZLE_INPUTS))

    print("Solution 1: {:}".format(knots.check_sequence()))
    print("Solution 2: {:}".format(full_knot_hash(PUZZLE_INPUTS)))
