# Advent of Code 2020, Day 21
# Michael Bell
# 12/21/2020
from collections import namedtuple
import helper


FoodItem = namedtuple('FoodItem', 'ingredients, allergens')

def parse_food_data(food_data):
    foods = []
    for food_contents in food_data:
        ingredients, allergens = food_contents.replace(')', '').split(' (contains ')
        ingredients = ingredients.split(' ')
        allergens = allergens.split(', ')

        foods.append(FoodItem(ingredients, allergens))
    
    return foods


def match_allergens_to_ingredients(foods):
    all_allergens = []
    for food in foods:
        all_allergens.extend(food.allergens)
    all_allergens = set(all_allergens)

    allergens_to_ingredients = {}
    for allergen in all_allergens:
        candidate_ingredients = None
        for food in foods:
            if allergen in food.allergens:
                if candidate_ingredients is None:
                    candidate_ingredients = set(food.ingredients)
                else:
                    candidate_ingredients = candidate_ingredients.intersection(set(food.ingredients))

        allergens_to_ingredients[allergen] = candidate_ingredients
    
    return allergens_to_ingredients


def find_non_allergenic_ingredients(foods, allergens_to_ingredients):
    all_ingredients = []
    for food in foods:
        all_ingredients.extend(food.ingredients)
    all_ingredients = set(all_ingredients)

    for allergen in allergens_to_ingredients:
        all_ingredients = all_ingredients.difference(allergens_to_ingredients[allergen])
    
    return all_ingredients


def count_ingredient_occurrences(foods, ingredients):
    count = 0
    for ingredient in ingredients:
        for food in foods:
            if ingredient in food.ingredients:
                count += 1
    return count


def get_dangerous_ingredient_list(foods, allergens_to_ingredients, non_allergenic_ingredients):
    a2i = []

    accounted_for_ingredients = set(non_allergenic_ingredients)
    while True:
        one_to_one = [
            (allergen, list(allergens_to_ingredients[allergen].difference(accounted_for_ingredients))[0]) 
            for allergen in allergens_to_ingredients 
            if len(allergens_to_ingredients[allergen].difference(accounted_for_ingredients)) == 1
        ]
        if len(one_to_one) == 0:
            break
        a2i.extend(one_to_one)
        accounted_for_ingredients = accounted_for_ingredients.union(set([o2o[1] for o2o in one_to_one]))

    return ','.join([v[1] for v in sorted(a2i, key=lambda x: x[0])])


### TESTS ###########################################################################
sample_food_data = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''.split('\n')

sample_food = parse_food_data(sample_food_data)
allergens_to_ingredients = match_allergens_to_ingredients(sample_food)
non_allergenic_ingredients = find_non_allergenic_ingredients(sample_food, allergens_to_ingredients)
assert count_ingredient_occurrences(sample_food, non_allergenic_ingredients) ==  5
assert get_dangerous_ingredient_list(sample_food, allergens_to_ingredients, non_allergenic_ingredients) == 'mxmxvkd,sqjhc,fvjkl'

### THE REAL THING ###################################################################
food_data = helper.read_input_lines(21)
foods = parse_food_data(food_data)
allergens_to_ingredients = match_allergens_to_ingredients(foods)
non_allergenic_ingredients = find_non_allergenic_ingredients(foods, allergens_to_ingredients)
print('Part 1:', count_ingredient_occurrences(foods, non_allergenic_ingredients))
print('Part 2:', get_dangerous_ingredient_list(foods, allergens_to_ingredients, non_allergenic_ingredients))
