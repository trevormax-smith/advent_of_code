# Advent of Code 2020, Day 11
# Michael Bell
# 12/11/2020

import helper

FLOOR = '.'
EMPTY_SEAT = 'L'
FILLED_SEAT = '#'


# Had this for part 1, but solution for part 2 was more general and solved both
# def count_neighboring_filled_seats(chart, i, j):

#     n_rows = len(chart)
#     n_cols = len(chart[0])

#     positions = [
#         (i+1, j-1),
#         (i+1, j),
#         (i+1, j+1),
#         (i, j-1),
#         (i, j+1),
#         (i-1, j-1),
#         (i-1, j),
#         (i-1, j+1)
#     ]

#     count = 0
#     for row, col in positions:
#         if row < 0 or col < 0 or row >= n_rows or col >= n_cols:
#             continue
#         elif chart[row][col] == FILLED_SEAT:
#             count += 1

#     return count


def count_filled_seats_los(chart, i, j, max_steps=1):

    n_rows = len(chart)
    n_cols = len(chart[0])

    directions = [
        (1, -1),
        (1, 0),
        (1, 1),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 0),
        (-1, 1)
    ]

    count = 0
    for d in directions:
        step = 1
        while max_steps is None or step <= max_steps:
            row = i + step * d[0]
            col = j + step * d[1]
            if row < 0 or col < 0 or row >= n_rows or col >= n_cols or chart[row][col] == EMPTY_SEAT:
                break
            elif chart[row][col] == FILLED_SEAT:
                count += 1
                break
            else:  # on a floor space
                step += 1
            
    return count


def count_filled_seats(chart):
    return sum(1 for row in chart for val in row if val == FILLED_SEAT)


def empty_chart(n_rows, n_cols):
    return [[' '] * n_cols for _ in range(n_rows)]


# Had this for part 1, but solution for part 2 was more general and solved both
# def update_seating_chart(chart):
#     n_rows = len(chart)
#     n_cols = len(chart[0])
#     new_chart = empty_chart(n_rows, n_cols)

#     for i, row in enumerate(chart):
#         for j, val in enumerate(row):
#             if val == FLOOR:
#                 new_chart[i][j] = FLOOR
#             elif val == EMPTY_SEAT and count_neighboring_filled_seats(chart, i, j) == 0:
#                 new_chart[i][j] = FILLED_SEAT
#             elif val == FILLED_SEAT and count_neighboring_filled_seats(chart, i, j) >= 4:
#                 new_chart[i][j] = EMPTY_SEAT
#             else:
#                 new_chart[i][j] = val

#     return new_chart


def update_seating_chart_los(chart, max_steps=1, get_up_thresh=4):
    n_rows = len(chart)
    n_cols = len(chart[0])
    new_chart = empty_chart(n_rows, n_cols)

    for i, row in enumerate(chart):
        for j, val in enumerate(row):
            if val == FLOOR:
                new_chart[i][j] = FLOOR
            elif val == EMPTY_SEAT and count_filled_seats_los(chart, i, j, max_steps) == 0:
                new_chart[i][j] = FILLED_SEAT
            elif val == FILLED_SEAT and count_filled_seats_los(chart, i, j, max_steps) >= get_up_thresh:
                new_chart[i][j] = EMPTY_SEAT
            else:
                new_chart[i][j] = val

    return new_chart


def copy_seating_chart(chart):
    n_rows = len(chart)
    n_cols = len(chart[0])
    new_chart = [[' '] * n_cols for _ in range(n_rows)]

    for i, row in enumerate(chart):
        for j, val in enumerate(row):
            new_chart[i][j] = val

    return new_chart


def are_charts_equal(chart1, chart2):

    for i, row in enumerate(chart1):
        for j, val in enumerate(row):
            if val != chart2[i][j]:
                return False

    return True


def print_chart(chart):
    for row in chart:
        print(''.join([c for c in row]))


def run(starting_chart, max_steps=1, get_up_thresh=4, verbose=False):
    chart = copy_seating_chart(starting_chart)
    n_iter = 0
    while True:
        
        if verbose:
            print(n_iter)
            print_chart(chart)
            _ = input('Hit enter')
            print()

        new_chart = update_seating_chart_los(chart, max_steps, get_up_thresh)
        if are_charts_equal(new_chart, chart):
            break
        else:
            chart = copy_seating_chart(new_chart)
        n_iter += 1
    
    return chart


sample_seating_chart = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''.split('\n')

sample_end_state = run(sample_seating_chart, verbose=True)
assert count_filled_seats(sample_end_state) == 37
sample_end_state_los = run(sample_seating_chart, None, 5, verbose=False)
assert count_filled_seats(sample_end_state_los) == 26

chart = helper.read_input_lines(11)
end_state = run(chart)
print("Part 1:", count_filled_seats(end_state))
end_state_los = run(chart, max_steps=None, get_up_thresh=5)
print('Part 2:', count_filled_seats(end_state_los))
