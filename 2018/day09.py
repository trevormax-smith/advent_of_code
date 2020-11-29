# Code for the 2019 AoC, day 9
# https://adventofcode.com/2019/day/9
# Michael Bell
# 12/9/2019


class Marble(object):
    """
    Essentially an item in a linked circular list.
    """
    def __init__(self, value):
        self.value = value
        self.cw_neighbor = None
        self.ccw_neighbor = None
    def __repr__(self):
        return f"Marble({self.value})"
    

def insert_cw_after(marble, new_marble):
    """
    For a given MARBLE, insert the NEW_MARBLE into the circle as MARBLE's neigbor 
    in the CW direction.
    """
    new_marble_ccw_neighbor = marble
    new_marble_cw_neighbor = marble.cw_neighbor

    new_marble.ccw_neighbor = new_marble_ccw_neighbor
    new_marble_ccw_neighbor.cw_neighbor = new_marble

    new_marble.cw_neighbor = new_marble_cw_neighbor
    new_marble_cw_neighbor.ccw_neighbor = new_marble


def remove_marble(marble):
    """
    Remove the given MARBLE from the circle of marbles.
    """
    marble.ccw_neighbor.cw_neighbor = marble.cw_neighbor
    marble.cw_neighbor.ccw_neighbor = marble.ccw_neighbor

    return marble.cw_neighbor


def play_marble_game(n_players, last_marble_value):
    """
    Given a number of players and number of marbles to play through, build up 
    the circle of marbles and tally up player scores according to the rules in the 
    challenge. Return the max score.
    """

    current_marble = Marble(0)
    current_marble.cw_neighbor = current_marble
    current_marble.ccw_neighbor = current_marble

    next_marble_value = 1
    current_player = 0
    player_scores = {player_id: 0 for player_id in range(n_players)}

    while next_marble_value <= last_marble_value: 
        if next_marble_value % 23 != 0:
            new_marble = Marble(next_marble_value)
            insert_cw_after(current_marble.cw_neighbor, new_marble)
            current_marble = new_marble
        else:
            player_scores[current_player] += next_marble_value

            marble_to_remove = current_marble
            for _ in range(7):
                marble_to_remove = marble_to_remove.ccw_neighbor
            player_scores[current_player] += marble_to_remove.value
            current_marble = remove_marble(marble_to_remove)

        # For testing
        # print_marble_circle(current_marble)

        current_player = (current_player + 1) % n_players
        next_marble_value += 1

    return max(player_scores.values())


def parse_game_spec(game_spec):
    """
    Parse the string specifying the number of players and max value of marble to play to.
    Return a tuple (N players, Max marble value)
    """

    pieces = game_spec.split()
    return int(pieces[0]), int(pieces[-2])


def print_marble_circle(marble):
    """
    Given any MARBLE in the circle, print the value of the marbles in the circle, starting from
    the 0th marble.
    """
    while marble.value != 0:
        marble = marble.cw_neighbor
    
    values = [marble.value]
    while marble.cw_neighbor.value != 0:
        marble = marble.cw_neighbor
        values.append(marble.value)
    
    print(' '.join([str(v) for v in values]))


if __name__ == '__main__':

    test_games = [
        parse_game_spec(game_spec) for game_spec in 
        '''10 players; last marble is worth 1618 points
13 players; last marble is worth 7999 points
17 players; last marble is worth 1104 points
21 players; last marble is worth 6111 points
30 players; last marble is worth 5807 points'''.split('\n')
    ]

    assert play_marble_game(9, 25) == 32

    test_game_max_scores = [8317, 146373, 2764, 54718, 37305]

    for spec, score in zip(test_games, test_game_max_scores):
        assert play_marble_game(*spec) == score

    game_spec = parse_game_spec('410 players; last marble is worth 72059 points')


    print(f"Solution 1: {play_marble_game(*game_spec)}")
    n_players, max_value = game_spec
    print(f"Solution 2: {play_marble_game(n_players, max_value * 100)}")
