# Code for the 2017 Advent Of Code, day 3
# http://adventofcode.com/2017
# Michael Bell
# 12/11/2017
# Answers validated

def count_steps(num):
    """
    Count steps of the Manhattan Distance from the origin to the given number
    when numbers are organized in a spiraling configuration like:

        17  16  15  14  13
        18   5   4   3  12
        19   6   1   2  11
        20   7   8   9  10
        21  22  23---> ...

    Return the number of steps (e.g. given 12, return 3)
    """

    (x, y) = square_to_grid(num)
    steps = abs(x) + abs(y)   

    return steps


def square_to_grid(num):

    if num == 1:
        return (0, 0)

    start_num = 1
    end_num = 2
    layer = 0

    while end_num <= num:
        layer += 1
        start_num = end_num
        end_num = start_num + 4 * (2 * layer + 1) - 4

    n_per_side = 2 * layer
    
    y = 1 - layer
    x = layer

    side = 0
    current_num = start_num

    while num > (current_num + n_per_side - 1):
        if side == 0:
            y += (n_per_side - 1)
            x -= 1
        elif side == 1:
            x -= (n_per_side - 1)
            y -= 1
        elif side == 2:
            y -= (n_per_side - 1)
            x += 1
        else:
            x += (n_per_side - 1)
        side += 1
        current_num += n_per_side

    if side == 0:
        y += (num - current_num)
    elif side == 1:
        x -= (num - current_num)
    elif side == 2:
        y -= (num - current_num)
    else:
        x += (num - current_num)

    return (x, y)


def first_value_larger_than(num):

    square = 2
    val = 1
    x = 1; y = 0
    grid = {(0, 0): 1}

    mods = [
        (-1,  1), (0,  1), (1,  1),
        (-1,  0),          (1,  0),
        (-1, -1), (0, -1), (1, -1) 
    ]

    while val <= num:
        val = 0
        for mod in mods:
            nbr_grid = (x + mod[0], y + mod[1])
            if nbr_grid in grid:
                val += grid[nbr_grid]

        grid[(x, y)] = val

        square += 1

        (x, y) = square_to_grid(square)

    return val


if __name__ == "__main__":

    print("Day 3")
    print("-"*5)

    # Tests
    assert count_steps(12) == 3
    assert count_steps(23) == 2
    assert count_steps(1024) == 31
    assert count_steps(25) == 4
    assert count_steps(26) == 5
    assert count_steps(17) == 4
    assert count_steps(19) == 2
    assert count_steps(1) == 0

    assert first_value_larger_than(1) == 2
    assert first_value_larger_than(2) == 4
    assert first_value_larger_than(7) == 10
    assert first_value_larger_than(329) == 330
    assert first_value_larger_than(330) == 351
    assert first_value_larger_than(750) == 806
    print("All tests passed")
    test_value = 312051 
    print("Solution 1: {:}".format(count_steps(test_value)))
    print("Solution 2: {:}".format(first_value_larger_than(test_value)))
