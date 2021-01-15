# Advent of Code 2015, Day 16
# Michael Bell
# 1/15/2021

import helper

def parse_aunts(aunt_list):
    
    aunts = {}

    for aunt_things in aunt_list:
        aunt_num = int(aunt_things[4:].split(':')[0])
        aunt_stuff = ": ".join(aunt_things[4:].split(': ')[1:]).split(', ')
        aunt_things = {}
        for thing in aunt_stuff:
            thing_name, quantity = thing.split(': ')
            quantity = int(quantity)
            aunt_things[thing_name] = quantity
        
        aunts[aunt_num] = aunt_things

    return aunts


def exactly_match(aunt_things, ticker_tape, thing):
    return aunt_things[thing] != ticker_tape[thing]


def matches_range(aunt_things, ticker_tape, thing):
    if thing in ['cats', 'trees']:
        return aunt_things[thing] <= ticker_tape[thing]
    elif thing in ['pomeranians', 'goldfish']:
        return aunt_things[thing] >= ticker_tape[thing]
    else:
        return aunt_things[thing] != ticker_tape[thing]


def find_aunt(ticker_tape, aunts, match_func=exactly_match):
    candidate_aunts = []

    for aunt_num in aunts:
        aunt_things = aunts[aunt_num]
        
        aunt_things_not_on_tape = set(aunt_things.keys()).difference(set(ticker_tape.keys()))
        if len(aunt_things_not_on_tape) > 0:
            continue

        match = True
        for thing in ticker_tape:
            if thing in aunt_things and match_func(aunt_things, ticker_tape, thing):
                match = False
                break
        if match:
            candidate_aunts.append(aunt_num)
    
    return candidate_aunts


aunts_sue = parse_aunts(helper.read_input_lines(16))
print('here')

ticker_tape = dict(
    children=3, cats=7, samoyeds=2, pomeranians=3, akitas=0, 
    vizslas=0, goldfish=5, trees=3, cars=2, perfumes=1
)

print('Part 1:', find_aunt(ticker_tape, aunts_sue))
print('Part 1:', find_aunt(ticker_tape, aunts_sue, matches_range))
