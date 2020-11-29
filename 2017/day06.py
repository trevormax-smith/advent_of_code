# Code for the 2017 Advent Of Code, day 6
# http://adventofcode.com/2017
# Michael Bell
# 12/12/2017
# Solutions passed 

def count_cycles_to_repeat(banks):

    banks = [int(b) for b in banks.split()]

    bank_history = []

    steps = 0

    while tuple(banks) not in bank_history:
        bank_history.append(tuple(banks))
        ndx = banks.index(max(banks))

        blocks = banks[ndx]
        banks[ndx] = 0

        while blocks > 0:
            ndx += 1
            ndx = ndx % len(banks)
            banks[ndx] += 1
            blocks -= 1

        steps += 1
    cycle_steps = steps - bank_history.index(tuple(banks))

    return steps, cycle_steps

if __name__ == "__main__":

    # TESTS

    test_banks = "0 2 7 0"

    assert count_cycles_to_repeat(test_banks)[0] == 5
    assert count_cycles_to_repeat(test_banks)[1] == 4

    print("All tests passed!")

    puzzle_banks = "4 1 15 12 0 9 9 5 5 8 7 3 14 5 12 3"

    print("Solution 1: {:}".format(count_cycles_to_repeat(puzzle_banks)[0]))
    print("Solution 2: {:}".format(count_cycles_to_repeat(puzzle_banks)[1]))
