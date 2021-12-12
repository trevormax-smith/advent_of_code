from os import read
from typing import List, Tuple
from helper import read_input, read_input_lines


def parse_height_map(raw_height_map: str) -> List[List[str]]:
    return [[int(h) for h in row] for row in raw_height_map.strip().split('\n')]


def is_oob(height_map: List[List[int]], point: Tuple[int, int]) -> bool:
    return not(0 <= point[0] < len(height_map) and 0 <= point[1] < len(height_map[0]))


def get_neighboring_points(point: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1)
    ]


def find_low_points(height_map: List[List[int]]) -> List[Tuple[int, int]]:

    low_points = []

    for row_num, row in enumerate(height_map):
        for col_num, height in enumerate(row):
            neighboring_points = get_neighboring_points((row_num, col_num))
            neighboring_points = [np for np in neighboring_points if not is_oob(height_map, np)]
            if all(height < height_map[np[0]][np[1]] for np in neighboring_points):
                low_points.append((row_num, col_num))

    return low_points


def get_point_risk_level(height_map: List[List[int]], point: Tuple[int, int]) -> int:
    return 1 + height_map[point[0]][point[1]]


def total_low_point_risk_level(height_map: List[List[int]]) -> int:
    low_points = find_low_points(height_map)
    return sum(get_point_risk_level(height_map, lp) for lp in low_points)


def find_basin_points(point: Tuple[int, int], height_map: List[List[int]], basin_points:List[Tuple[int, int]]) -> None:
    if height_map[point[0]][point[1]] < 9:
        basin_points.append(point)
        neighboring_points = get_neighboring_points(point)
        neighboring_points = [np for np in neighboring_points if not is_oob(height_map, np) and not np in basin_points]
        for np in neighboring_points:
            find_basin_points(np, height_map, basin_points)
    return None


def get_product_of_largest_basin_sizes(height_map: List[List[int]], n_largest_basins: int=3) -> int:
    basin_sizes = []
    low_points = find_low_points(height_map)
    for lp in low_points:
        basin_points = []
        find_basin_points(lp, height_map, basin_points)
        # For some reason I end up with dupes in my list, using set to eliminate
        # Ideally would fix recursion to avoid dupes but this works
        basin_sizes.append(len(set(basin_points)))  
    basin_sizes = sorted(basin_sizes, reverse=True)
    prod = 1
    for bs in basin_sizes[:n_largest_basins]:
        prod *= bs
    return prod


if __name__ == '__main__':

    ### THE TEST
    test_height_map = '''2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    '''
    test_height_map = parse_height_map(test_height_map)
    assert total_low_point_risk_level(test_height_map) == 15
    assert get_product_of_largest_basin_sizes(test_height_map) == 1134

    ### THE REAL THING
    height_map = parse_height_map(read_input())
    print(f'Part 1: {total_low_point_risk_level(height_map)}')
    print(f'Part 2: {get_product_of_largest_basin_sizes(height_map)}')
