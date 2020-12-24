# Advent of Code 2020, Day 22
# Michael Bell 
# 12/22/2020

import helper


def parse_decks(deck_data):
    decks = []

    for card_list in deck_data.split('\n\n'):
        deck = []
        for card in card_list.split('\n')[1:]:
            if card.strip():
                deck.append(int(card))
        decks.append(deck)

    return decks


def combat(starting_decks, recursive=False, game_num=1, verbose=False):

    # Deep copy so we aren't altering the decks as passed in below
    decks = [d.copy() for d in starting_decks]

    if verbose:
        print(f'=== Game {game_num} ===\n')

    round_number = 1

    # Keep a list of deck configurations seen before so we know to end game if we're going to loop
    previous_decks = []

    while all(len(d) > 0 for d in decks):
        if verbose:
            print(f'-- Round {round_number} (Game {game_num}) --')
            for i, deck in enumerate(decks):
                print(f"Player {i + 1}'s deck:", ', '.join([str(d) for d in deck]))

        if recursive:
            if decks in previous_decks:
                if verbose:
                    print(f'Found loop in Game {game_num}, round {round_number}')
                return 0, None
            else:
                previous_decks.append([deck.copy() for deck in decks])

        cards_played = [d.pop(0) for d in decks]

        if recursive and all(len(d) >= cp for cp, d in zip(cards_played, decks)):
            if verbose:
                print('Playing a sub-game to determine the winner...\n')
            winner, _ = combat([d[:cp] for cp, d in zip(cards_played, decks)], recursive=True, game_num=game_num + 1, verbose=verbose)
        else:
            winner = cards_played.index(max(cards_played))

        if verbose:
            for i, card in enumerate(cards_played):
                print(f"Player {i + 1} plays:", card)
            print(f"Player {winner + 1} wins the round!\n")

        decks[winner].append(cards_played.pop(winner))
        decks[winner].append(cards_played.pop())

        round_number += 1

    if recursive and game_num > 1:
        if verbose:
            print(f'...anyway, back to game {game_num-1}.')
        return [i for i, d in enumerate(decks) if len(d) > 0][0], None
        

    if verbose:
        print('\n== Post-game results ==')

    score = 0
    winner = None
    for i, deck in enumerate(decks):
        if verbose:    
            print(f"Player {i+1}'s deck:", ', '.join([str(d) for d in deck]))

        if len(deck) > 0:
            winner = i
            score += sum((i + 1) * c for i, c in enumerate(deck[::-1]))
    
    if verbose:
        print(f'\nFinal score: {score}')

    return winner, score


### TESTS #####################################
sample_input = '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''
decks = parse_decks(sample_input)
assert combat(decks, verbose=False)[1] == 306

_, score = combat(decks, recursive=True, verbose=False)
assert score == 291

sample_input = '''Player 1:
43
19

Player 2:
2
29
14
'''
decks = parse_decks(sample_input)
# _, score = combat(decks, verbose=True, recursive=True)

### THE REAL THING ############################
real_input = helper.read_input(22)
decks = parse_decks(real_input)
print("Part 1:", combat(decks)[1])
print("Part 2:", combat(decks, recursive=True)[1])
