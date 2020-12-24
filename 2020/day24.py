# Advent of Code 2020, Day 24
# Michael Bell
# 12/24/2020
from collections import defaultdict
import helper


neighbor_directions = ['e', 'se', 'sw', 'w', 'nw', 'ne']  # Add 3 to get index of opposite direction


def flip_tiles(all_directions):
    tiles = defaultdict(lambda: 0)

    for directions in all_directions:
        
        remaining_directions = directions
        coordinates = (0, 0)
        while len(remaining_directions) > 0:
            for i, nd in enumerate(neighbor_directions):
                if remaining_directions[:len(nd)] == nd:
                    if nd == 'e':
                        coordinates = (coordinates[0] + 2, coordinates[1])
                    elif nd == 'w':
                        coordinates = (coordinates[0] - 2, coordinates[1])
                    elif nd == 'se':
                        coordinates = (coordinates[0] + 1, coordinates[1] - 1)
                    elif nd == 'sw':
                        coordinates = (coordinates[0] - 1, coordinates[1] - 1)
                    elif nd == 'ne':
                        coordinates = (coordinates[0] + 1, coordinates[1] + 1)
                    elif nd == 'nw':
                        coordinates = (coordinates[0] - 1, coordinates[1] + 1)
                    
                    remaining_directions = remaining_directions[len(nd):]
        
        tiles[coordinates] = (tiles[coordinates] + 1) % 2
    
    return tiles


def count_black_tiles(tiles):
    '''
    Return the total count of black tiles (those w/ value 1) in the set of tiles.
    '''
    return sum(tiles[i] for i in tiles)


def count_neihboring_black_tiles(tiles, coords):
    '''
    Count the number of black tiles in the hex grid locations around the given coords.
    '''
    black_tiles = 0
    for d_coords in [(2, 0), (-2, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nc = (coords[0] + d_coords[0], coords[1] + d_coords[1])
        if nc in tiles:
            black_tiles += tiles[nc]
    return black_tiles


def fill_neighboring_white_tiles(tiles):
    '''
    For every black tile in the set of tiles, make sure every neighboring tile is in the set of tiles. Add 
    implied white tiles where needed.
    '''
    black_tile_coords = [tc for tc in tiles if tiles[tc] == 1]
    
    for btc in black_tile_coords:
        for d_coords in [(2, 0), (-2, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nc = (btc[0] + d_coords[0], btc[1] + d_coords[1])
            tiles[nc] += 0


def evolve_tiles(tiles, days=100, verbose=False):

    for day in range(1, days + 1):

        new_tiles = defaultdict(lambda: 0)

        fill_neighboring_white_tiles(tiles)

        for tile_coords in tiles:
            neighboring_black_tiles = count_neihboring_black_tiles(tiles, tile_coords)
            if tiles[tile_coords] == 1 and (neighboring_black_tiles == 0 or neighboring_black_tiles > 2):
                new_tiles[tile_coords] = 0
            elif tiles[tile_coords] == 0 and neighboring_black_tiles == 2:
                new_tiles[tile_coords] = 1
            else:
                new_tiles[tile_coords] = tiles[tile_coords]
        
        tiles = new_tiles

        if verbose and (day <= 10 or (day % 10) == 0):
            print(f'Day {day}:', count_black_tiles(tiles))

    return new_tiles
    

### TESTS #####################################################
example_instructions = '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew'''.split('\n')

tiles = flip_tiles(example_instructions)

black_tiles = count_black_tiles(tiles)
assert black_tiles == 10

tiles = evolve_tiles(tiles, verbose=False)
black_tiles = count_black_tiles(tiles)
assert black_tiles == 2208

### THE REAL THING ###############################
instructions = helper.read_input_lines(24)
tiles = flip_tiles(instructions)

black_tiles = count_black_tiles(tiles)
print('Part 1:', black_tiles)

tiles = evolve_tiles(tiles)
black_tiles = count_black_tiles(tiles)
print('Part 2:', black_tiles)
