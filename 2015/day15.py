# Advent of Code 2015, Day 15
# Michael Bell
# 1/14/2021

import helper


class Ingredient(object):
    def __init__(self, properties):
        name, properties = properties.split(': ')
        prop_scores = properties.split(', ')
        self.properties = {}
        for ps in prop_scores:
            p, s = ps.split(' ')
            self.properties[p] = int(s)
        self.name = name
    def __repr__(self):
        return f'Ingredient<{self.name}>'


def cookie_score(recipe):
    '''
    Here recipe is a dict keyed on Ingredients with value of # of tsps in the recipe.
    '''
    prod = 1
    for prop in ['capacity', 'durability', 'flavor', 'texture']:
        total = 0
        for ingredient in recipe:
            total += recipe[ingredient] * ingredient.properties[prop]
        total = max([0, total])
        prod *= total
    return prod


def count_calories(recipe):
    return sum(ingredient.properties['calories'] * recipe[ingredient] for ingredient in recipe)


def optimize_recipe(ingredient_properties, calorie_count=None):

    ingredients = [Ingredient(properties) for properties in ingredient_properties]

    total_tsp = 100

    n_ingredients = len(ingredients)

    def recursive_for(remaining_tsp, ingredients, best, calorie_count, recipe=None): 

        if len(ingredients) >= 1:
            if recipe is None:
                this_recipe = {}
            else:
                this_recipe = recipe.copy()

            if len(ingredients) == 1:
                this_recipe[ingredients[0]] = remaining_tsp
                recursive_for(0, ingredients[1:], best, calorie_count, this_recipe)
            else:
                for i in range(remaining_tsp):
                    this_recipe[ingredients[0]] = i
                    recursive_for(remaining_tsp - i, ingredients[1:], best, calorie_count, this_recipe)
        else:
            recipe_score = cookie_score(recipe)
            if recipe_score > best['score'] and (calorie_count is None or count_calories(recipe) == calorie_count):
                best['score'] = recipe_score
                best['recipe'] = recipe.copy()
    
    best = {'recipe': None, 'score': -1}
    recursive_for(total_tsp, ingredients, best, calorie_count)

    return best['score'], best['recipe']

example_ingredients = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''.split('\n')

ingredients = [Ingredient(properties) for properties in example_ingredients]
recipe = {ingredients[0]: 44, ingredients[1]: 56}
assert cookie_score(recipe) == 62842880
recipe = {ingredients[0]: 40, ingredients[1]: 60}
assert cookie_score(recipe) == 57600000
assert count_calories(recipe) == 500
assert optimize_recipe(example_ingredients)[0] == 62842880
assert optimize_recipe(example_ingredients, 500)[0] == 57600000

ingredient_list = helper.read_input_lines(15)
best_score, best_recipe = optimize_recipe(ingredient_list)
print('Part 1:', best_score, best_recipe)
best_score, best_recipe = optimize_recipe(ingredient_list, 500)
print('Part 2:', best_score, best_recipe)
