# Advent of Code, 2015
# Day 2
# 11/29/2020
# from itertools import combinations


def combinations(it, _):

    combos = []
    for n, i in enumerate(it):
        for j in it[(n+1):]:
            combos.append((i, j))

    return combos


def parse_box_dims(dims):
    return tuple([int(d) for d in dims.split('x')])


def paper_area(box_dims):
    
    area = 0 
    smallest_side = None

    for (x, y) in combinations(box_dims, 2):
        side_area = x * y
        area += side_area * 2
        if not smallest_side or side_area < smallest_side:
            smallest_side = side_area

    return area + smallest_side


def ribbon_length(box_dims):

    box_volume = 1
    for box_dim in box_dims:
        box_volume *= box_dim
    
    shortest_perimeter = None
    for (x, y) in combinations(box_dims, 2):
        perimeter = 2 * x + 2 * y
    
        if not shortest_perimeter or perimeter < shortest_perimeter:
            shortest_perimeter = perimeter

    return shortest_perimeter + box_volume


def total_ribbon_length(multiple_box_dims):
    return sum(ribbon_length(box_dims) for box_dims in multiple_box_dims)


def total_paper_area(multiple_box_dims):
    return sum(paper_area(box_dims) for box_dims in multiple_box_dims)


if __name__ == '__main__':

    assert parse_box_dims('2x3x5') == (2, 3, 5)

    assert paper_area(parse_box_dims('2x3x4')) == 58
    assert ribbon_length(parse_box_dims('2x3x4')) == 34

    with open('./inputs/day02.txt', 'r') as f:
        box_dims = [parse_box_dims(line) for line in f.readlines() if line.strip()]
    
    print('Total area:', total_paper_area(box_dims))
    print('Total length:', total_ribbon_length(box_dims))
