# Advent of Code 2020, Day 7
# Michael Bell
# 12/7/2020
from typing import List, Tuple
import helper

def parse_regulation(reg: str) -> Tuple[int, str]:
    '''Parse a single line of the bag regulations'''

    outer_bag, inner_bags = reg.replace('bags', '').replace('bag', '').replace('.', '').split('contain')

    outer_bag = outer_bag.strip()  # Get rid of any trailing spaces, outer bag is all set now

    # Inner bags is a comma sep list of quantities and bag colors, or says "no other bags" if none are contained
    inner_bags = [ib.strip() for ib in inner_bags.split(',')]
    if len(inner_bags) == 1 and inner_bags[0] == 'no other':
        inner_bags = []
    inner_bags = [
        (int(ib.split(' ')[0]), ib.replace(ib.split(' ')[0], '').strip()) 
        for ib in inner_bags
    ]
    
    return outer_bag, inner_bags  # A color string and a tuple of (quantity, color string)


def parse_regulations(regs: List[str]) -> List[Tuple[int, str]]:
    '''
    Parse a list of regulations, where each line has a bag color and its required contents.
    '''
    regs = [parse_regulation(reg) for reg in regs]
    regs = {r[0]: r[1] for r in regs}
    return regs


def can_contain_color(regs: List[Tuple[int, str]], outer_bag: str, color: str) -> bool:
  
    if len(regs[outer_bag]) == 0:
        # We've hit the end of the line
        return False
    else:
        for ib in regs[outer_bag]:
            if ib[1] == color or can_contain_color(regs, ib[1], color):
                return True
        return False


def count_required_bags(regs: List[Tuple[int, str]], color: str) -> int:
    bag_count = 0
    for ib in regs[color]:
        bag_count += ib[0] * (1 + count_required_bags(regs, ib[1]))
    return bag_count


def bags_that_can_contain(regs: List[Tuple[int, str]], color: str) -> List[str]:
    return [ob for ob in regs if can_contain_color(regs, ob, color)]


### TESTS ###############################################################################
sample_regulations = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''.split('\n')
regs = parse_regulations(sample_regulations)
sample_gold_containers = bags_that_can_contain(regs, 'shiny gold')
assert len(sample_gold_containers) == 4
assert (
    'bright white' in sample_gold_containers 
    and 'muted yellow' in sample_gold_containers 
    and 'dark orange' in sample_gold_containers 
    and 'light red' in sample_gold_containers
)
assert count_required_bags(regs, 'shiny gold') == 32

sample_regulations = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''.split('\n')
regs = parse_regulations(sample_regulations)
assert count_required_bags(regs, 'shiny gold') == 126


### THE REAL THING #######################################################################
regulations = helper.read_input_lines(7)
regs = parse_regulations(regulations)
gold_containers = bags_that_can_contain(regs, 'shiny gold')
print('Part 1:', len(gold_containers))
print('Part 2:', count_required_bags(regs, 'shiny gold'))
