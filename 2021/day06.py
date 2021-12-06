from typing import List, Dict
from helper import read_input


new_fish_spawn_timer = 8
spawn_timer = 6


def parse_fish(fish: str) -> List[int]:
    return [int(v) for v in fish.split(',')]


def naive_simulation(fish: List[int], days: int) -> List[int]:
    
    simulated_fish = fish.copy()

    for d in range(days):
        new_fish = []
        for i, timer in enumerate(simulated_fish):
            if timer == 0:
                new_fish.append(new_fish_spawn_timer)
                next_timer = spawn_timer
            else:
                next_timer = timer - 1
            simulated_fish[i] = next_timer
        simulated_fish.extend(new_fish)
    
    return simulated_fish


def make_fish_tracker() -> Dict[int, int]:
    return {timer: 0 for timer in range(new_fish_spawn_timer + 1)}


def scalable_simulation(fish: List[int], days: int) -> int:
    fish_tracker = make_fish_tracker()
    for timer in fish:
        fish_tracker[timer] += 1

    for d in range(days):
        next_fish_tracker = make_fish_tracker()        
        for timer in range(new_fish_spawn_timer):
            next_fish_tracker[timer] = fish_tracker[timer + 1]
        next_fish_tracker[new_fish_spawn_timer] = fish_tracker[0]
        next_fish_tracker[spawn_timer] += fish_tracker[0]
        fish_tracker = next_fish_tracker.copy()

    return sum(fish_tracker[timer] for timer in fish_tracker)


### TESTS
test_fish = parse_fish('3,4,3,1,2')
assert len(naive_simulation(test_fish, 18)) == 26
assert len(naive_simulation(test_fish, 80)) == 5934

assert scalable_simulation(test_fish, 18) == 26
assert scalable_simulation(test_fish, 80) == 5934


### THE REAL THING
fish = parse_fish(read_input(6).strip())
print(f'Part 1: {len(naive_simulation(fish, 80))}')
print(f'Part 2: {scalable_simulation(fish, 256)}')
