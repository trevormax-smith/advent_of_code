# Advent of Code, 2015
# Day 1
# 11/29/2020

def what_floor(instructions): 
    '''
    Given instructions as a sequence of open or closed parentheses, e.g. "()())()()"
    return a the floor that you end up on. Open paren means go up one floor. Close
    paren means go down one floor. You start on floor 0.
    '''

    current_floor = 0
    first_visits_basement_at = 0

    for instruction_number, instruction in enumerate(instructions):
        if instruction == "(":
            current_floor = current_floor + 1
        elif instruction == ')':
            current_floor = current_floor - 1
        else:
            raise ValueError(f"Unexpected instruction encountered {instruction}")
        
        if first_visits_basement_at == 0 and current_floor < 0:
            first_visits_basement_at = instruction_number + 1

    return current_floor, first_visits_basement_at 


if __name__ == "__main__":

    # Write some tests of our floor counter function
    test_instructions = ")())())" 

    assert what_floor(test_instructions) == (-3, 1)

    with open('./inputs/day01.txt', 'r') as f:
        instructions = f.read()
    
    final_floor, first_basement_at = what_floor(instructions)
    print(f"You ended up on floor {final_floor}")
    print(f"You first went to the basement at step {first_basement_at}")
