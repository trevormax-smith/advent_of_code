from os import read
from typing import List, Tuple, Callable
from helper import read_input
from day06 import parse_fish
from time import time


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


def optimizer2(crab_positions: List[int], fuel_cost_func: Callable) -> Tuple[int, int]:
    '''
    Assuming the optimization is convex, which it is in the tests
    5x faster than the one above on the tests
    '''
    # Pick the average as a starting position because why not
    last_position = sum(crab_positions) // len(crab_positions)
    direction = 1
    last_fuel = fuel_cost_func(crab_positions, last_position)
    steps = 0

    while True:
        next_position = last_position + direction
        next_fuel = fuel_cost_func(crab_positions, next_position)
        if next_fuel > last_fuel and steps == 0:
            # Going in the wrong direction to start
            direction *= -1
        elif next_fuel > last_fuel:
            # If we have been going downhill and start going up, we've found the bottom
            return last_position, last_fuel
        else:
            # Keep going down hill
            last_position, last_fuel = next_position, next_fuel
        steps += 1


### TEST
test_crab_positions = parse_fish('16,1,2,0,4,2,7,1,2,14')
test_position, test_cost = optimize_position(test_crab_positions, constant_fuel_cost)
assert test_position == 2
assert test_cost == 37

t0 = time()
test_position, test_cost = optimizer2(test_crab_positions, growing_fuel_cost)
print(time() - t0)

t0 = time()
test_position, test_cost = optimize_position(test_crab_positions, growing_fuel_cost)
print(time() - t0)

assert test_position == 5
assert test_cost == 168

### THE REAL THING
crab_positions = parse_fish(read_input(7))
print(f'Part 1: {optimizer2(crab_positions, constant_fuel_cost)[1]}')
print(f'Part 2: {optimizer2(crab_positions, growing_fuel_cost)[1]}')
