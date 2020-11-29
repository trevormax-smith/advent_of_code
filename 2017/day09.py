# Code for the 2017 Advent Of Code, day 9
# http://adventofcode.com/2017
# Michael Bell
# 12/16/2017
# Solutions passed!

def score_stream(stream):
    """
    Given a stream of groups (characters between {}), return the total score for the stream.
    'Garbage' sequences (things between <>) are ignored, as are characters following !.
    """

    group_scores = []
    current_level = 0
    garbage_characters = 0

    garbage_open = False
    cancel_next_char = False

    for char in stream:
        if cancel_next_char:
            cancel_next_char = False
            continue
        if char == "!":
            cancel_next_char = True
        elif garbage_open:
            if char == '>':
                garbage_open = False
            else:
                garbage_characters += 1
        elif char == "{":
            current_level += 1
        elif char == "}":
            group_scores.append(current_level)
            current_level -= 1
        elif char == "<":
            garbage_open = True

    return sum(group_scores), garbage_characters


with open('data/day09_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read().replace('\r', '').replace('\n', '').strip()


if __name__ == '__main__':

    assert score_stream('{}')[0] == 1
    assert score_stream('{{{}}}')[0] == 6
    assert score_stream('{{},{}}')[0] == 5
    assert score_stream('{{{},{},{{}}}}')[0] == 16
    assert score_stream('{<a>,<a>,<a>,<a>}')[0] == 1
    assert score_stream('{{<ab>},{<ab>},{<ab>},{<ab>}}')[0] == 9
    assert score_stream('{{<!!>},{<!!>},{<!!>},{<!!>}}')[0] == 9
    assert score_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}')[0] == 3
    assert score_stream('{{<a!>},{<a!>},{<a!>},{<ab>}}')[1] == 17

    print('All tests passed!')

    print('Solution 1: {:}'.format(score_stream(PUZZLE_INPUT)[0]))
    print('Solution 2: {:}'.format(score_stream(PUZZLE_INPUT)[1]))
