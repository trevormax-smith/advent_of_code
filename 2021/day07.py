from os import read
from typing import List, Tuple, Callable
from helper import read_input
from day06 import parse_fish


def constant_fuel_cost(crab_positions: List[int], ref_position: int) -> int:
    return sum(abs(p-ref_position) for p in crab_positions)


def growing_fuel_cost(crab_positions: List[int], ref_position: int) -> int:
    return sum([sum([step for step in range(1, abs(p-ref_position)+1)]) for p in crab_positions])


def optimize_position(crab_positions: List[int], fuel_cost_func: Callable) -> Tuple[int, int]:
    optimal_positions_and_costs = {}

    for test_position in range(min(crab_positions), max(crab_positions)):
        optimal_positions_and_costs[test_position] = fuel_cost_func(crab_positions, test_position)

    optimal_position = min(optimal_positions_and_costs, key=lambda x: optimal_positions_and_costs[x])

    return optimal_position, optimal_positions_and_costs[optimal_position]


### TEST
test_crab_positions = parse_fish('16,1,2,0,4,2,7,1,2,14')
test_position, test_cost = optimize_position(test_crab_positions, constant_fuel_cost)
assert test_position == 2
assert test_cost == 37
test_position, test_cost = optimize_position(test_crab_positions, growing_fuel_cost)
assert test_position == 5
assert test_cost == 168

### THE REAL THING
crab_positions = parse_fish(read_input(7))
print(f'Part 1: {optimize_position(crab_positions, constant_fuel_cost)[1]}')
print(f'Part 1: {optimize_position(crab_positions, growing_fuel_cost)[1]}')
