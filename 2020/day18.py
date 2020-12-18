# Advent of Code 2020, Day 18
# Michael Bell
# 12/18/2020

import helper


def evaluate(exp: str, advanced=False) -> int:

    # Find indices of top level parentheses so I can grab inner expressions
    paren_stack = []
    paren_pairs = []
    for i, char in enumerate(exp):
        if char == '(':
            paren_stack.append(i)
        elif char == ')':
            last_open_position = paren_stack.pop()
            if not paren_stack:
                paren_pairs.append((last_open_position, i))
    
    # Evaluate sub-expressions w/in parens, rebuild expression without parens
    new_exp = ''
    ref = 0
    for paren_pair in paren_pairs:
        new_exp += exp[ref:paren_pair[0]]
        sub_exp = exp[(paren_pair[0] + 1):paren_pair[1]]
        sub_exp_result = evaluate(sub_exp, advanced=advanced)
        new_exp += str(sub_exp_result)
        ref = paren_pair[1] + 1
    new_exp += exp[ref:]

    # Now the expression is just a flat list of integers and operations
    # Evaluate additions first if in advanced mode, replace triplets with results of the addition
    exp_pieces = new_exp.split(' ')
    if advanced:
        while '+' in exp_pieces:
            first_plus = exp_pieces.index('+')
            result = str(int(exp_pieces[first_plus - 1]) + int(exp_pieces[first_plus + 1]))
            exp_pieces = exp_pieces[:(first_plus-1)] + [result] + exp_pieces[(first_plus + 2):]

    # Now the expression is just a flat list of integers and operations... evaluate left to right
    # If advanced mode, the only remaining operations will be multiplication
    val = int(exp_pieces[0])
    exp_pieces = exp_pieces[1:]
    while len(exp_pieces) >= 2:
        val2 = int(exp_pieces[1])
        if exp_pieces[0] == '+':
            val += val2
        elif exp_pieces[0] == '*':
            val *= val2
        else:
            raise ValueError(f'Unexpected operator {exp_pieces[1]}')
        exp_pieces = exp_pieces[2:]
        
    return val


### TESTS #################################################################
assert evaluate("1 + 2 * 3 + 4 * 5 + 6") == 71
assert evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert evaluate('2 * 3 + (4 * 5)') == 26
assert evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

assert evaluate("1 + 2 * 3 + 4 * 5 + 6", True) == 231
assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', True) == 51
assert evaluate('2 * 3 + (4 * 5)', True) == 46
assert evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)', True) == 1445
assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', True) == 669060
assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', True) == 23340

### THE REAL THING ########################################################
expressions = helper.read_input_lines(18)
total = sum(evaluate(expression) for expression in expressions)
print('Part 1:', total)
total = sum(evaluate(expression, True) for expression in expressions)
print('Part 2:', total)
