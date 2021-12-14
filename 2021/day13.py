from ast import parse
from dataclasses import dataclass
from typing import List, Tuple
import helper


other_axis = {'x': 'y', 'y': 'x'}


@dataclass
class Dot:
    x: int
    y: int

    # Need the `__eq__` and `__hash__` to make this class 
    # hashable so that I can use `set`
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash(str(self))


@dataclass
class Fold:
    axis: str
    value: int

    def do_fold(self, dots: List[Dot]) -> List[Dot]:
        folded_dots = []
        for dot in dots:
            if getattr(dot, self.axis) < self.value:
                folded_dots.append(dot)
            else:
                # Getting unnecessarily cute here
                folded_value = self.value - (getattr(dot, self.axis) - self.value)
                other_value = getattr(dot, other_axis[self.axis])
                folded_dot = Dot(0, 0)
                setattr(folded_dot, self.axis, folded_value)
                setattr(folded_dot, other_axis[self.axis], other_value)
                folded_dots.append(folded_dot)
        return list(set(folded_dots))


def parse_dots_and_folds(puzzle_input: str) -> Tuple[List[Dot], List[Fold]]:

    dot_input, fold_input = puzzle_input.strip().split('\n\n')
    
    dots = [
        Dot(*[int(v) for v in line.split(',')]) 
        for line in dot_input.split('\n')
    ]

    folds = []
    for line in fold_input.split('\n'):
            axs, val = line.replace('fold along ', '').split('=')
            folds.append(Fold(axs, int(val)))
    
    return dots, folds


def print_dots(dots: List[Dot]) -> None:

    max_x = max(dots, key=lambda x: x.x).x
    max_y = max(dots, key=lambda x: x.y).y

    to_plot = [[' '] * (max_x + 1) for _ in range(max_y + 1)]
    for dot in dots:
        to_plot[dot.y][dot.x] = '#'

    for row in to_plot:
        print(''.join(row))


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''

    test_dots, test_folds = parse_dots_and_folds(test_input)
    assert len(test_folds[0].do_fold(test_dots)) == 17

    ### THE REAL THING
    puzzle_input = helper.read_input()
    dots, folds = parse_dots_and_folds(puzzle_input)
    folded_dots = folds[0].do_fold(dots)
    print(f'Part 1: {len(folded_dots)}')

    for fold in folds[1:]:
        folded_dots = fold.do_fold(folded_dots)

    print(f'Part 2:')
    print_dots(folded_dots)
