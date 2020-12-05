# Advent of Code 2020, Day 5
# Michael Bell 
# 12/5/2020
import helper
import math
import time

N_ROWS = 128
N_COLS = 8


def bsp_1d(code):

    lower = 0
    upper = 2 ** len(code) - 1
    for char in code:
        mid = lower + (upper - lower + 1) // 2 - 1
        if char == '0':
            upper = mid
        elif char == '1':
            lower = mid + 1
        else:
            raise ValueError(f'Invalid Code {char}')
    assert lower == upper
    row = lower

    return row


def seat_decode(code):
    row_spec_len = int(math.log2(N_ROWS))
    col_spec_len = int(math.log2(N_COLS))
    assert len(code) == row_spec_len + col_spec_len
    row_spec = code[:row_spec_len].replace('F', '0').replace('B', '1')
    col_spec = code[-col_spec_len:].replace('L', '0').replace('R', '1')

    row = bsp_1d(row_spec)
    col = bsp_1d(col_spec)

    return row, col


def seat_id(code):
    row, col = seat_decode(code)
    return row * N_COLS + col


def find_missing_seat(seat_ids):
    seat_ids = sorted(seat_ids)
    current_value = seat_ids[0] - 1
    for i, seat_id in enumerate(seat_ids):
        current_value += 1
        if seat_id != current_value and seat_ids[i-1] == current_value - 1 and seat_id == current_value + 1:
            return current_value
    return -1


def find_missing_seat2(seat_ids):
    # This method would be nicely vectorizable, and it's cleaner anyway
    seat_ids = sorted(seat_ids)
    for l, r in zip(seat_ids[:-1], seat_ids[1:]):
        if r-l == 2:
            return (r + l) // 2
    return -1


### TESTS #################################
assert seat_decode('FBFBBFFRLR') == (44, 5)
assert seat_id('FBFBBFFRLR') == 357

assert seat_decode('BFFFBBFRRR') == (70, 7)
assert seat_id('BFFFBBFRRR') == 567

assert seat_decode('FFFBBBFRRR') == (14, 7)
assert seat_id('FFFBBBFRRR') == 119

assert seat_decode('BBFFBBFRLL') == (102, 4)
assert seat_id('BBFFBBFRLL') == 820


### THE REAL THING ########################
seat_codes = helper.read_input_lines(5)
seat_ids = [seat_id(code) for code in seat_codes]
highest_seat_id = max(seat_ids)
print('Part 1:', highest_seat_id)

print('Part 2:', find_missing_seat(seat_ids))
print('Part 2 v2:', find_missing_seat2(seat_ids))
