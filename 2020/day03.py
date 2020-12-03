# Advent of Code 2020, Day 3
# Michael Bell
# 12/3/2020


class TreeMap(object):
    TREE = '#'
    OPEN = '.'

    def __init__(self, tree_pattern: str):
        self.tree_pattern = [line for line in tree_pattern.split('\n') if line.strip()]
        self.map_height = len(self.tree_pattern)
        self.map_width = len(self.tree_pattern[0])
        
    def check_for_tree(self, row: int, col: int):
        return self.tree_pattern[row][col % self.map_width] == self.TREE

    def count_trees_on_path(self, path_down, path_right):
        current_col = path_right
        current_row = path_down
        n_trees = 0

        while current_row < self.map_height:
            if self.check_for_tree(current_row, current_col):
                n_trees += 1
            current_row += path_down
            current_col += path_right

        return n_trees


def check_paths(tree_map: TreeMap) -> int:
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    prod = 1
    for slope in slopes:
        prod *= tree_map.count_trees_on_path(*slope)
    return prod


sample_pattern = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

tree_map = TreeMap(sample_pattern)
assert not tree_map.check_for_tree(1, 3)
assert tree_map.check_for_tree(2, 6)
assert tree_map.check_for_tree(7, 21)

assert tree_map.count_trees_on_path(1, 3) == 7
assert check_paths(tree_map) == 336

with open('./inputs/day03.txt', 'r') as f:
    tree_pattern = f.read()

tree_map = TreeMap(tree_pattern)
print('Part 1:', tree_map.count_trees_on_path(1, 3))
print('Part 2:', check_paths(tree_map))
