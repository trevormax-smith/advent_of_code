from collections import defaultdict
from typing import Tuple, List, Union
from math import sqrt
from helper import read_input_lines


class VentLine(object):

    def __init__(self, vent_line_def: str) -> None:
        vent_line_def_parsed = vent_line_def.split(' -> ')
        self.starting_point, self.ending_point = [tuple([int(val) for val in vent_line_def_parsed[i].split(',')]) for i in range(2)]
        self._points: Union[None, List[Tuple[int]]] = None

    def is_diagonal(self) -> bool:
        return (
            (self.starting_point[0] != self.ending_point[0]) and 
            (self.starting_point[1] != self.ending_point[1])
        )

    @property
    def line_length(self) -> float:
        return sqrt(
            (self.ending_point[0] - self.starting_point[0]) ** 2 + 
            (self.ending_point[1] - self.starting_point[1]) ** 2
        )

    @property
    def points(self) -> List[Tuple[int]]:
        if not self._points:
            line_length = self.line_length
            step_size = sqrt(2) if self.is_diagonal() else 1.0
            # Should always be an int, but rounding and casting to enforce
            n_steps = int(line_length / step_size + 0.5) + 1  
            self._points = [
                # + 0.5 and cast to int to round off any floating point errors
                tuple([int(self.starting_point[ndx] + i * step_size * (self.ending_point[ndx] - self.starting_point[ndx]) / line_length + 0.5) for ndx in range(2)]) for i in range(n_steps)
            ]
        return self._points


def parse_vent_lines(vent_line_defs: List[str]) -> List[VentLine]:
    return [VentLine(vent_line_def) for vent_line_def in vent_line_defs]


def count_overlaps(vent_lines: List[VentLine], count_diagonals: bool=False) -> int:
    point_counts = defaultdict(lambda: 0)
    for vent_line in vent_lines:
        if not vent_line.is_diagonal() or count_diagonals:
            for point in vent_line.points:
                point_counts[point] += 1

    return sum(1 for point in point_counts if point_counts[point] > 1)


### TESTS
test_vent_line_defs = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''.split('\n')
test_vent_lines = parse_vent_lines(test_vent_line_defs)

assert test_vent_lines[1].is_diagonal()
assert not test_vent_lines[0].is_diagonal()
assert test_vent_lines[0].line_length == 5
assert count_overlaps(test_vent_lines) == 5
assert count_overlaps(test_vent_lines, True) == 12

### THE REAL THING
vent_line_defs = read_input_lines(5)
vent_lines = parse_vent_lines(vent_line_defs)
print(f'Part 1: {count_overlaps(vent_lines)}')
print(f'Part 2: {count_overlaps(vent_lines, True)}')
