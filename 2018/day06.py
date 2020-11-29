# Code for the 2018 AoC, day 6
# https://adventofcode.com/2018/day/6
# Michael Bell
# 12/6/2018
import sys
import tqdm
from collections import defaultdict


def dict_keymin(d):
    """
    Given a dictionary of arbitrary keys and integer values >= 0, return the keys of the min
    item with the min value. If more than one value is the minimum, all keys are returned with 
    that value. The return value is always a list, even if the min is unique.
    """
    min_k = [sys.maxsize]
    min_v = sys.maxsize
    for k in d:
        v = d[k]
        if v < min_v:
            min_v = v
            min_k = [k]
        elif v == min_v:
            min_k.append(k)
    return min_k


def manhatan_distance(coord1, coord2):

    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def parse_coordinates(coordinate_list):
    lines = coordinate_list.split('\n')
    coordinates = []
    for line in lines:
        tmp = line.split(',')
        coordinates.append((
            int(tmp[0]), int(tmp[1].strip())
        ))
    return coordinates


def make_grid_of_nearest_coordinates(coordinates):
    """
    Fill a grid of the coordinate ID of the nearest of the given coordinates using the Manhattan 
    distance. If two coordinates are equidistant, the cell is filled with -1, indicating that no
    unique coordinate is closest to the cell.
    """

    n_cols = max(coordinates, key=lambda x: x[0])[0] + 1
    n_rows = max(coordinates, key=lambda x: x[1])[1] + 1

    dist_grid = [[None for i in range(n_cols)] for j in range(n_rows)]

    for col in tqdm.tqdm(range(n_cols)):
        for row in range(n_rows):
            coord_dists = {}
            grid_coordinate = (col, row)
            for i, coordinate in enumerate(coordinates):
                coord_dists[i] = manhatan_distance(grid_coordinate, coordinate)
    
            closest_coordinate = dict_keymin(coord_dists)
            if len(closest_coordinate) == 1:
                dist_grid[row][col] = closest_coordinate[0]
            else:
                dist_grid[row][col] = -1 

    return dist_grid


def print_grid(dist_grid):

    for row in dist_grid:
        print(' '.join([f'{cell:3}' for cell in row]))


def largest_non_inf_area(dist_grid):

    # Coordinates whos neiboring area extends to the edge of the grid have infinite area
    # We will exclude these later
    coords_w_infinite_area = set(
        dist_grid[0] + dist_grid[1] + 
        [cell[0] for cell in dist_grid] + 
        [cell[-1] for cell in dist_grid]
    )

    coordinate_areas = defaultdict(int)
    for row in dist_grid[1:-1]:
        for col in row[1:-1]:
            if col >= 0 and col not in coords_w_infinite_area:
                coordinate_areas[col] += 1
    
    return max(coordinate_areas.values())


def make_total_distance_grid(coordinates):

    n_cols = max(coordinates, key=lambda x: x[0])[0] + 1
    n_rows = max(coordinates, key=lambda x: x[1])[1] + 1

    dist_grid = [[0 for i in range(n_cols)] for j in range(n_rows)]

    for col in tqdm.tqdm(range(n_cols)):
        for row in range(n_rows):
            grid_coordinate = (col, row)
            for i, coordinate in enumerate(coordinates):
                dist_grid[row][col] += manhatan_distance(grid_coordinate, coordinate)

    return dist_grid


def show_cells_within_total_dist(total_distance_grid, threshold):
    mask_grid = [
        [0 for i in range(len(total_distance_grid[0]))] for j in range(len(total_distance_grid))
    ]

    for row_num, row in enumerate(total_distance_grid):
        for col_num, col in enumerate(row):
            if col < threshold:
                mask_grid[row_num][col_num] = 1

    print_grid(mask_grid)


def area_within_total_dist(total_distance_grid, threshold):
    mask_grid = [
        [0 for i in range(len(total_distance_grid[0]))] for j in range(len(total_distance_grid))
    ]
    area = 0
    for row_num, row in enumerate(total_distance_grid):
        for col_num, col in enumerate(row):
            if col < threshold:
                area += 1

    return area

    
if __name__ == '__main__':

    test_coordinate_list = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''

    test_coordinates = parse_coordinates(test_coordinate_list)
    test_dist_grid = make_grid_of_nearest_coordinates(test_coordinates)
    print_grid(test_dist_grid)
    assert largest_non_inf_area(test_dist_grid) == 17

    test_total_dist_grid = make_total_distance_grid(test_coordinates)
    show_cells_within_total_dist(test_total_dist_grid, 32)
    assert area_within_total_dist(test_total_dist_grid, 32) == 16

    with open('./data/day06_input.txt', 'r') as f:
        input1 = f.read()

    coordinates = parse_coordinates(input1)
    dist_grid = make_grid_of_nearest_coordinates(coordinates)
    print(f'Solution 1: {largest_non_inf_area(dist_grid)}') 
    total_dist_grid = make_total_distance_grid(coordinates)
    print(f'Solution 2: {area_within_total_dist(total_dist_grid, 10_000)}')