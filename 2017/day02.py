# Code for the 2017 Advent Of Code, day 2
# http://adventofcode.com/2017
# Michael Bell
# 12/9/2017
# Solutions valid


def row_ratio(vals):
    for j, v in enumerate(vals):
        for w in vals[(j+1):]:
            num = max([v, w])
            den = min([v, w])

            if num % den == 0:
                return (num // den)
    raise ValueError('No pairs found.') 


def checksum(spreadsheet, mode='minmax'):
    """
    Given a string SPREADSHEET with multiple lines of numbers separated by
    spaces, and each line ending with a newline character, return the 
    sum of the difference between the max and min values of each line.
    """

    rows = spreadsheet.split('\n')

    diffs = []
    for i, row in enumerate(rows):
        if len(row) == 0:
            continue
        vals = [int(n) for n in row.strip('\n').split()]
        if mode == 'minmax':
            diffs.append(max(vals) - min(vals))
        elif mode == 'div':
            diffs.append(row_ratio(vals)) 
    return sum(diffs)

test_input1 = """5 1 9 5
7 5 3
2 4 6 8"""
test_input2 = """5 9 2 8
9 4 7 3
3 8 6 5"""

with open('data/day02_input.txt', 'r') as f:
    real_input = f.read()

if __name__ == "__main__":
    
    assert checksum(test_input1) == 18
    assert checksum(test_input2, 'div') == 9
    print('All tests pass')
    
    print("Checksum 1: {:}".format(checksum(real_input)))
    print("Checksum 2: {:}".format(checksum(real_input, 'div')))
