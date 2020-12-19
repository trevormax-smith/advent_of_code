# Advent of Code 2020, Day 19
# Michael Bell
# 12/19/2020

from itertools import product
import helper


def parse_input(inp):
    rule_defs, messages = inp.split('\n\n')

    messages = [m for m in messages.split('\n') if m]

    rules = {}

    for rule_def in rule_defs.split('\n'):
        num, rule = rule_def.split(': ')
        num = int(num)
        

        if '"' in rule:
            rule_set = rule.replace('"', '')
        else:
            rule_set = []
            rule_parts = rule.split(' | ')
            for rule_part in rule_parts:
                rule_set.append([int(rp) for rp in rule_part.split(' ')])
    
        rules[num] = rule_set

    return rules, messages


def resolve_rule(rules, num):

    if isinstance(rules[num], str):
        return [rules[num]]
    else:
        results = []
        for option in rules[num]:
            resolved_parts = [resolve_rule(rules, rule_num) for rule_num in option]
            
            # if isinstance(resolved_parts[0], str):
            #     resolved_parts = ''.join(resolved_parts)
            #     results.append(resolved_parts)
            # else:
            products = list(product(*resolved_parts))
            resolved_parts = [''.join(p) for p in products]
            results.extend(resolved_parts)
            
        return results


def count_matching_messages(msgs, rules, rule_num):
    rule = resolve_rule(rules, rule_num)
    rule = set(rule)  # For speedy lookups

    rule_match_count = 0
    for m in msgs:
        if m in rule:
            rule_match_count += 1

    return rule_match_count


def get_chunks(string, chunk_len):
    chunks = []
    for i in range(0, len(string), chunk_len):
        chunks.append(string[i:i+chunk_len])
    return chunks


def part2(msgs, rules):
    # This only works for this specific set of rules, and to count matches specifically to rule 0
    # Rule 0 is 
    #   0: 8 11
    # Replacing rule 8 with 
    #   8: 42 | 42 8
    # and rule 11 with
    #   11: 42 31 | 42 11 31
    # Rule 0 now loops (since 8 and 11 are self referrential) and can match an infinite set of messages
    # Both rule 8 and 11 boil down to a set of products of options from rules 42 and 31
    # Both of rules 42 and 31 are resolvable (they don't loop), so we can resolve a set of options for
    # those two rules.
    # Rule 0 is then made up of a product of options between rules 8 and 11
    # Rules 31 and 42 are sets of strings of length N
    # Rule 8 effectively matches any string where all sub-strings of length N are within the set of options from rule 42
    #       It can be 42 | 42 42 | 42 42 42 | ...
    # Rule 11 effectively matches any string where, when cut in half, the first half set of sub-strings of length N are 
    # within the set of options for rule 42 and the second half are within the set of options from rule 31
    #       It can be 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | ...
    # So to match rule 0, we have to have a set of length N substrings at the end of the message that match options w/in rule 31,
    # another equal length set of substrings preceding those that match rule 42, then at least one extra substring of length N 
    # at the start that is within the set of rule 42 options.
    # So rule 0 can be
    #       42 42 31 | 42 42 42 31 31 | 42 42 42 31 | 42 42 42 42 31 31 | ... 

    rule31 = resolve_rule(rules, 31)
    rule42 = resolve_rule(rules, 42)

    # I'm not sure if this has to be true generally, but I'm going to be assuming it is below
    assert len(rule31[0]) == len(rule42[0])
    chunk_len = len(rule31[0])

    rule31 = set(rule31)
    rule42 = set(rule42)
    # This must be true... not sure there is a soln if it's not
    assert len(rule42.intersection(rule31)) == 0

    match_count = 0

    for msg in msgs:

        # We're going to be checking chunks of length chunk_len substrings to see if they are in the 
        # sets of rule31 or rule42
        chunks = get_chunks(msg, chunk_len)
        
        # The smallest matching message would have to have at least 3 chunks (one at the start matching rule 42, and a pair, first matching 42 then 31)
        # If we can't at least pass this criteria, move along
        if len(chunks) < 3 or chunks[0] not in rule42 or chunks[-1] not in rule31:
            continue
        else:
            # Now find the chunks at the end of the lsit of chunks that are in the set of rule 31 options
            chunks = chunks[1:]
            matches31count = 0
            for c in chunks[::-1]:
                if c not in rule31:
                    break
                else:
                    matches31count += 1
            chunks = chunks[:-matches31count]
            
            # I have to have at least the same number of chunks as we had that match rule 31
            # and they all have to be found within the set of options for rule 42
            if len(chunks) >= matches31count and all(c in rule42 for c in chunks):
                match_count += 1

    return match_count


### TESTS ##################################################
sample_input = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''
rules, msgs = parse_input(sample_input)
rule_0_match_count = count_matching_messages(msgs, rules, 0)
assert rule_0_match_count == 2


sample_input = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''
rules, msgs = parse_input(sample_input)
rule_0_match_count = count_matching_messages(msgs, rules, 0)
assert rule_0_match_count == 3

assert part2(msgs, rules) == 12

# rules[8] = [[42], [42, 8]]
# rules[11] = [[42, 31], [42, 11, 31]]

# rule42 = resolve_rule(rules, 42)
# rule31 = resolve_rule(rules, 31)

# rule_0_match_count = count_matching_messages(msgs, rules, 0)
# assert rule_0_match_count == 12


### THE REAL THING ############################################
actual_input = helper.read_input(19)
rules, msgs = parse_input(actual_input)
rule_0_match_count = count_matching_messages(msgs, rules, 0)
print("Part 1:", rule_0_match_count)
print("Part 2:", part2(msgs, rules))
