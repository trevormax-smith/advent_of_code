# Code for the 2018 AoC, day 12
# https://adventofcode.com/2018/day/12
# Michael Bell
# 12/12/2018
from collections import defaultdict
from tqdm import tqdm


def parse_initial_state(state_spec):

    spec_lines = state_spec.split('\n')

    plant_states = defaultdict(bool)
    evolutionary_rules = defaultdict(bool)

    for spec_line in spec_lines:
        if spec_line.strip() == '':
            continue
        if 'state' in spec_line:
            initial_state_spec = spec_line.split(':')[1].strip()

            for i, pot in enumerate(initial_state_spec):
                if pot == '#':
                    plant_states[i] = True

        else:
            config, result = spec_line.split(' => ')
            if result.strip() == '#':
                config_as_bools = tuple([char == '#' for char in config.strip()])
                evolutionary_rules[config_as_bools] = True

    return plant_states, evolutionary_rules


def evolve_one_generation(plant_states, rules):

    next_gen = defaultdict(bool)

    occupied_pots = {k: plant_states[k] for k in plant_states if plant_states[k]}

    min_num = min(occupied_pots.keys()) - 4
    max_num = max(occupied_pots.keys()) + 5

    for plant_num in range(min_num, max_num):

        local_neigborhood = tuple([plant_states[plant_num + i] for i in range(-2, 3)])
        if rules[local_neigborhood]:
            next_gen[plant_num] = True

    return next_gen


def evolve_n_generations(plant_states, rules, n, store_all=False):
    if store_all:
        generations = [plant_states]
    else:
        generations = None

    gen = plant_states

    for _ in tqdm(range(n)):
        gen = evolve_one_generation(gen, rules)
        
        if store_all:
            generations.append(gen)

        # If we hit a state where all plants are dead, we will stay there
        if all(not gen[k] for k in gen):
            return gen, generations

    return gen, generations


def print_plants(plants):

    plant_chars = []

    occupied_pots = {k: plants[k] for k in plants if plants[k]}

    # Always include the 0th plant when printing
    min_num = min((min(occupied_pots.keys()) - 2, 0))
    max_num = max((max(occupied_pots.keys()) + 3, 0))

    for k in range(min_num, max_num):

        if k == 0:
            plant_chars.append(' {:} '.format('#' if plants[k] else '.'))
        else:
            plant_chars.append('{:}'.format('#' if plants[k] else '.'))
    print(''.join(plant_chars))


def print_generations(gens):
    for i, gen in enumerate(gens):
        print(f'{i}: ', end='')
        print_plants(gen)
    print()


def sum_plant_pot_nums(plants):
    return sum([k for k in plants if plants[k]])


if __name__ == '__main__':

    test_initial_state_spec = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''
    test_initial_state, test_rules = parse_initial_state(test_initial_state_spec)

    test_generation, test_generations = evolve_n_generations(
        test_initial_state, test_rules, 20, True
    )
    print_generations(test_generations)

    assert sum_plant_pot_nums(test_generations[-1]) == 325

    with open('./data/day12_input.txt', 'r') as f:
        input1 = f.read()
    
    init_state, rules = parse_initial_state(input1)
    last_gen, gens = evolve_n_generations(init_state, rules, 20)
    print(f'Solution 1: {sum_plant_pot_nums(last_gen)}')

    # This ain't happening! It'll take 3K hours w/ current implementation
    # A bare for loop (only w/ a pass) would take 3 hours, so optimizing the evolution step will
    # not help
    # There has to be a way to solve w/out iterating 50_000_000_000 times
    # last_gen, _ = evolve_n_generations(init_state, rules, 50000000000)
    # print(f'Solution 2: {sum_plant_pot_nums(last_gen)}')

    # Let's try running for some iterations to see how the score changes over time.
    # It might converge to zero, or hit some steady state that will allow us to infer the 
    # end state directly.

    last_gen, gens = evolve_n_generations(init_state, rules, 5000, True)
    scores = []
    for gen in gens:
        scores.append(sum_plant_pot_nums(gen))
    with open('./data/day12_test_output.txt', 'w') as f:
        f.write('\n'.join([str(s) for s in scores]))

    # It turns out you reach a steady state rate of growth in the score. After about 85 iterations
    # the sum of plant pots increases by exactly 50 points each step. So you can work out that the 
    # score after 50_000_000_000 iterations is 2500000000695 for the given input