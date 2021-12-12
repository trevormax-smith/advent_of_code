from typing import List, Tuple, Dict
import helper
from day09 import get_neighboring_points, is_oob


def parse_energy_grid(energy_levels: str) -> List[List[int]]:
    return [
        [int(v) for v in row]
        for row in energy_levels.split('\n')
    ]


def find_flashers(
    energy_grid: List[List[int]]
) -> List[Tuple[int, int]]:
    flashers = []
    for row_num, row in enumerate(energy_grid):
        for col_num, energy_level in enumerate(row):
            if energy_level == 10:
                flashers.append((row_num, col_num))
    return flashers


def get_neighbors(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    neighbors = []
    for row_mod in range(-1, 2):
        for col_mod in range(-1, 2):
            neighbors.append((cell[0] + row_mod, cell[1] + col_mod))
    neighbors.remove(cell)
    return neighbors


def reset_flashers(energy_grid: List[List[int]]) -> List[List[int]]:
    return [
        [v if v <= 9 else 0 for v in row]
        for row in energy_grid
    ]


def update_energy_grid(energy_grid: List[List[int]]) -> List[List[int]]:
    updated_energy_grid = [
        [v + 1 for v in row]
        for row in energy_grid
    ]

    flashers = find_flashers(updated_energy_grid)
    while flashers:
        for flasher in flashers:
            # Prevents this flasher from being counted again
            updated_energy_grid[flasher[0]][flasher[1]] += 1
            neighbors = get_neighbors(flasher)
            for neighbor in neighbors:
                if not is_oob(updated_energy_grid, neighbor) and updated_energy_grid[neighbor[0]][neighbor[1]] != 10:
                    updated_energy_grid[neighbor[0]][neighbor[1]] += 1
        flashers = find_flashers(updated_energy_grid)
    
    updated_energy_grid = reset_flashers(updated_energy_grid)

    return updated_energy_grid


def simulate_steps(energy_grid: List[List[int]], n_steps: int=100) -> Tuple[int, int]:
    '''
    If n_steps == -1, continues until the first step when every grid point flashes.
    '''
    flash_count = 0
    steps = 0
    grid_size = len(energy_grid) * len(energy_grid[0])
    while True:
        energy_grid = update_energy_grid(energy_grid)
        these_flashes = sum([
            sum([1 for v in row if v == 0])
            for row in energy_grid
        ])
        flash_count += these_flashes
        steps += 1

        if (n_steps > 0 and steps == n_steps) or (n_steps < 0 and these_flashes == grid_size):
            break

    return flash_count, steps


### THE TESTS
test_energy_levels = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''
test_energy_grid = parse_energy_grid(test_energy_levels)
assert simulate_steps(test_energy_grid, 10)[0] == 204
assert simulate_steps(test_energy_grid)[0] == 1656
assert simulate_steps(test_energy_grid, -1)[1] == 195

### THE REAL THING
puzzle_input = helper.read_input()
energy_grid = parse_energy_grid(puzzle_input)
print(f'Part 1: {simulate_steps(energy_grid)[0]}')
print(f'Part 2: {simulate_steps(energy_grid, -1)[1]}')
