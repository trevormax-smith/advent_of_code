"""
2017 Advent Of Code, day 25
https://adventofcode.com/2017/day/25
Michael Bell
12/29/2017
"""

from collections import defaultdict


TEST_INPUT = '''Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
'''


def parse_blueprint(blueprint):

    states = {}

    checksum_after = None
    starting_state = None

    blueprint = blueprint.replace('\r', '').split('\n')

    current_state = None
    current_value = None
    instruction = dict()

    for line in blueprint:
        if not line:  # Skip blank lines
            continue

        if 'Begin' in line:
            starting_state = line.split()[3].replace('.', '')
        elif 'Perform' in line:
            checksum_after = int(line.split()[5])
        elif 'In' in line:
            current_state = line.replace(':', '').split()[2]
        elif 'If' in line:
            instruction = dict()
            current_value = int(line.strip().replace(':', '').split()[5])
        elif 'Write' in line:
            instruction['write'] = int(line.strip().replace('.', '').split()[4])
        elif 'Move' in line:
            instruction['move'] = -1 if line.strip().replace('.', '').split()[6] == 'left' else 1
        elif 'Continue' in line:
            instruction['next_state'] = line.strip().replace('.', '').split()[4]
        
        if len(instruction) == 3:
            if current_state not in states:
                states[current_state] = {current_value: instruction}
            else:
                states[current_state][current_value] = instruction
    
    return states, starting_state, checksum_after


def execute_blueprint(states, starting_state, checksum_after):

    tape = defaultdict(int)
    slot = 0
    current_state = starting_state

    # print(0, current_state, slot, tape)

    for step in range(checksum_after):
        instruction = states[current_state][tape[slot]]

        tape[slot] = instruction['write']
        slot += instruction['move']
        current_state = instruction['next_state']

        # print(step + 1, current_state, slot, tape)
    
    return sum(tape[x] for x in tape)


with open('data/day25_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()

if __name__ == '__main__':

    assert execute_blueprint(*parse_blueprint(TEST_INPUT)) == 3
    print('All tests passed')
    print('Solution 1: {:}'.format(execute_blueprint(*parse_blueprint(PUZZLE_INPUT))))
