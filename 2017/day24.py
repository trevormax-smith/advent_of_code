"""
2017 Advent Of Code, day 24
https://adventofcode.com/2017/day/24
Michael Bell
12/29/2017
"""


def parse_piece(piece_def):
    return tuple(int(val) for val in piece_def.split('/'))


def get_pieces(piece_defs):
    # Pieces are all unique
    return set(
        parse_piece(piece_def) for piece_def in piece_defs.replace('\r', '').split('\n')
        if piece_def
    )


def get_connecting_pieces(connector, pieces):
    candidate_connections = set()
    
    for piece in pieces:
        if piece[0] == connector or piece[1] == connector:
            candidate_connections.add(piece)

    return candidate_connections


def get_bridge_strengths(open_connector, pieces):
    
    if not pieces:
        return []

    possible_connecting_pieces = get_connecting_pieces(open_connector, pieces)

    strengths = []

    for possible_connecting_piece in possible_connecting_pieces:

        new_connector = possible_connecting_piece[0] \
            if possible_connecting_piece[0] != open_connector \
            else possible_connecting_piece[1]

        other_pieces = pieces.difference([possible_connecting_piece])

        this_connection_strengths = get_bridge_strengths(new_connector, other_pieces)

        if not this_connection_strengths:
            strengths.append(possible_connecting_piece[0] + possible_connecting_piece[1])
        else:
            strengths.extend([
                tcs + possible_connecting_piece[0] + possible_connecting_piece[1] 
                for tcs in this_connection_strengths
            ])

    return strengths


def get_bridge_strengths_lengths(open_connector, pieces):
    
    if not pieces:
        return []

    possible_connecting_pieces = get_connecting_pieces(open_connector, pieces)

    strengths = []

    for possible_connecting_piece in possible_connecting_pieces:

        new_connector = possible_connecting_piece[0] \
            if possible_connecting_piece[0] != open_connector \
            else possible_connecting_piece[1]

        other_pieces = pieces.difference([possible_connecting_piece])

        this_connection_strengths = get_bridge_strengths_lengths(new_connector, other_pieces)

        if not this_connection_strengths:
            strengths.append(
                (possible_connecting_piece[0] + possible_connecting_piece[1], 1)
            )
        else:
            strengths.extend([
                (tcs[0] + possible_connecting_piece[0] + possible_connecting_piece[1], tcs[1] + 1) 
                for tcs in this_connection_strengths
            ])

    return strengths


with open('data/day24_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


def get_strongest_longest_bridge(strengths_lengths):

    longest_length = -1
    strongest_strength = -1
    strongest_longest_bridge = None

    for strength_length in strengths_lengths:
        if ((strength_length[1] > longest_length) or (strength_length[1] == longest_length and strength_length[0] > strongest_strength)):
            strongest_longest_bridge = strength_length
            longest_length = strength_length[1]
            strongest_strength = strength_length[0]
    
    return strongest_longest_bridge


if __name__ == '__main__':

    pieces = get_pieces(PUZZLE_INPUT)

    possible_strengths = get_bridge_strengths(0, pieces)
    print('Solution 1: {:}'.format(max(possible_strengths)))

    possible_strengths_lengths = get_bridge_strengths_lengths(0, pieces)
    strongest_longest = get_strongest_longest_bridge(possible_strengths_lengths)
    print('Solution 2: {:}'.format(strongest_longest[0]))
