# Code for the 2018 AoC, day 14
# https://adventofcode.com/2018/day/14
# Michael Bell
# 12/14/2018


def create_new_recipes(recipes, current1, current2):
    combined_recipe_scores = recipes[current1] + recipes[current2]
    recipes.extend([int(c) for c in str(combined_recipe_scores)])


def next_recipe(recipes, current1, current2):
    current1 = (current1 + recipes[current1] + 1) % len(recipes)
    current2 = (current2 + recipes[current2] + 1) % len(recipes)

    return current1, current2


def advance_n_recipes(recipes, current1, current2, n, verbose=False):

    recipes = [r for r in recipes]

    for _ in range(n):
        if verbose:
            print_state(recipes, current1, current2)
        create_new_recipes(recipes, current1, current2)
        current1, current2 = next_recipe(recipes, current1, current2)

    return recipes, current1, current2


def print_state(recipes, current1, current2):

    to_print = []
    for i, c in enumerate(recipes):
        if current1 == i:
            to_print.append(f'({c})')
        elif current2 == i:
            to_print.append(f'[{c}]')
        else:
            to_print.append(f' {c} ')

    print(''.join(to_print))


def get_next_m_after_n(recipes, c1, c2, n, m=10):

    recipes, c1, c2 = advance_n_recipes(
        recipes, c1, c2, n + m + 1
    )

    return ''.join(str(r) for r in recipes[n:n + m])


def get_n_recipes_until(recipes, c1, c2, score_pattern, verbose=False):

    recipes = [r for r in recipes]

    first_int = int(score_pattern[0])
    score_ints = [int(s) for s in score_pattern]
    score_len = len(score_pattern)

    while True:
        if (
            len(recipes) > score_len and recipes[-score_len] == first_int 
            and recipes[-score_len:] == score_ints 
        ):
            return len(recipes) - score_len
        elif (  # Because we can add 2 scores in one iteration, we need to check two positions
            len(recipes) > (score_len+1) and recipes[-score_len - 1] == first_int 
            and recipes[-score_len-1:-1] == score_ints
        ):
            return len(recipes) - score_len - 1

        create_new_recipes(recipes, c1, c2)
        c1, c2 = next_recipe(recipes, c1, c2)

        if verbose and len(recipes) % 1000000 == 0:
            print(f"{len(recipes)} tried so far")


if __name__ == '__main__':

    recipes = [3, 7]
    c1 = 0
    c2 = 1    

    # recipes, c1, c2 = advance_n_recipes(
    #     recipes, current_recipe_elf1, current_recipe_elf2, 10, True
    # )

    assert get_next_m_after_n(recipes, c1, c2, 9) == '5158916779'
    assert get_next_m_after_n(recipes, c1, c2, 5) == '0124515891'
    assert get_next_m_after_n(recipes, c1, c2, 18) == '9251071085'
    assert get_next_m_after_n(recipes, c1, c2, 2018) == '5941429882'

    assert get_n_recipes_until(recipes, c1, c2, '51589') == 9
    assert get_n_recipes_until(recipes, c1, c2, '01245') == 5
    assert get_n_recipes_until(recipes, c1, c2, '92510') == 18
    assert get_n_recipes_until(recipes, c1, c2, '59414') == 2018
    assert get_n_recipes_until(recipes, c1, c2, '5158916779') == 9
    assert get_n_recipes_until(recipes, c1, c2, '5891') == 11

    input1 = 323081

    print(f'Solution 1: {get_next_m_after_n(recipes, c1, c2, input1)}')
    print(f'Solution 2: {get_n_recipes_until(recipes, c1, c2, str(input1), True)}')
