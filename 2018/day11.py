# Code for the 2018 AoC, day 11
# https://adventofcode.com/2018/day/11
# Michael Bell
# 12/11/2018
from tqdm import tqdm
from joblib import Parallel, delayed
import sys


def dict_keymax(d):
    """
    Given a dictionary of arbitrary keys and integer values >= 0, return the key of the max
    item with the max value.
    """
    max_k = sys.maxsize * -1
    max_v = sys.maxsize * -1
    for k in d:
        v = d[k]
        if v > max_v:
            max_v = v
            max_k = k
    return max_k


def compute_power(x, y, sn):

    rack_id = x + 10
    power = rack_id * (rack_id * y + sn)
    power = int((power / 100) % 10)  # Keep only the hundreds digit

    return power - 5


def make_power_grid(nx, ny, sn):
    power_grid = []
    for y in range(ny):
        row = []
        for x in range(nx):
            row.append(compute_power(x+1, y+1, sn))
        power_grid.append(row)
    return power_grid


def get_patch(power_grid, x, y, nx=3, ny=3):

    patch = []
    for row in power_grid[(y - 1):(y - 1 + ny)]:
        patch_row = [val for val in row[(x - 1):(x - 1 + nx)]]
        patch.append(patch_row)
    
    return patch


def get_total_power(grid):
    total_power = 0
    for row in grid:
        total_power += sum(row)
    return total_power


def find_max_power_patch(grid, patch_size=3):

    powers = {}
    slicer = slice(None, -patch_size+1) if patch_size > 1 else slice(None, None)

    for y, row in enumerate(grid[slicer]):
        for x, val in enumerate(row[slicer]):
            patch = get_patch(grid, x+1, y+1, patch_size, patch_size)
            powers[(x+1, y+1)] = get_total_power(patch)

    max_power_loc = dict_keymax(powers)
    max_power = max(powers.values())

    return (max_power_loc[0], max_power_loc[1], patch_size), max_power


def find_max_power_patch_any_size(grid):
    """
    This is super slow!
    """

    powers = Parallel(n_jobs=8)(
        delayed(find_max_power_patch)(grid, patch_size)
        for patch_size in tqdm(range(1, 301))
    )

    max_power_config = max(powers, key=lambda x: x[1])

    return max_power_config


if __name__ == '__main__':

    assert compute_power(3, 5, 8) == 4
    assert compute_power(122, 79, 57) == -5
    assert compute_power(217, 196, 39) == 0
    assert compute_power(101, 153, 71) == 4

    test_grid1 = make_power_grid(300, 300, 18)
    test_patch1 = get_patch(test_grid1, 33, 45)
    assert test_patch1[0] == [4, 4, 4]  
    assert test_patch1[-1] == [1, 2, 4]
    assert get_total_power(test_patch1) == 29

    test_grid2 = make_power_grid(300, 300, 42)
    test_patch2 = get_patch(test_grid2, 21, 61) 
    assert test_patch2[0] == [4, 3, 3]
    assert test_patch2[-1] == [3, 3, 4]
    assert get_total_power(test_patch2) == 30

    loc1, pwr1 = find_max_power_patch(test_grid1)
    assert (loc1[0], loc1[1]) == (33, 45) and pwr1 == 29

    loc1, pwr1 = find_max_power_patch(test_grid1, 16)
    assert (loc1[0], loc1[1]) == (90, 269) and pwr1 == 113

    # cfg1, pwr1 = find_max_power_patch_any_size(test_grid1)
    # assert cfg1 == (90,269,16) and pwr1 == 113

    loc2, pwr2 = find_max_power_patch(test_grid2)
    assert (loc2[0], loc2[1]) == (21, 61) and pwr2 == 30

    # cfg2, pwr2 = find_max_power_patch_any_size(test_grid2)
    # assert cfg2 == (232,251,12) and pwr2 == 119

    grid = make_power_grid(300, 300, 7347)
    loc, pwr = find_max_power_patch(grid)
    print(f"Solution 1: ({loc[0]}, {loc[1]})  (power={pwr})")

    cfg, pwr = find_max_power_patch_any_size(grid)
    print(f"Solution 2: ({cfg[0]},{cfg[1]},{cfg[2]})  (power={pwr})")
