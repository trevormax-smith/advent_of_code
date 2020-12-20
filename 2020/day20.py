# Advent of Code 2020, Day 20
# Michael Bell
# 12/20/2020

import helper


def init_image(n_rows, n_cols):
    return [[' '] * n_cols for _ in range(n_rows)]
    

def get_dims(image):
    return len(image), len(image[0])


def transpose(image):
    
    n_rows, n_cols = get_dims(image)
    new_image = init_image(n_cols, n_rows)  # flip columns and rows, so an MxN becomes NxM

    for row_num in range(n_rows):
        for col_num in range(n_cols):
            target_row = col_num
            target_col = row_num
            new_image[target_row][target_col] = image[row_num][col_num]

    return new_image


def check_neighbor(ref_image, other_image, direction, reorient=True):
    # return None if not a match, otherwise return the other_image, perhaps re-oriented if allowed
    pass


# Need a function to turn linked array into array of image IDs
# Need a function to turn an array of image IDs and a dict of images into one large image


def display(image, title=None):
    if title:
        print(title)
    for row in image:
        print(' '.join(row))
    print()


def flip(image, axis=0):
    
    n_rows, n_cols = get_dims(image)
    new_image = init_image(n_rows, n_cols)
    
    for row_num in range(n_rows):
        for col_num in range(n_cols):
            target_row = n_rows - row_num - 1 if axis == 0 else row_num
            target_col = n_cols - col_num - 1 if axis == 1 else col_num
            new_image[target_row][target_col] = image[row_num][col_num]

    return new_image


def rotate(image, direction='CW'):

    new_image = transpose(image)
    flip_axis = 0 if direction == 'CCW' else 1
    return flip(new_image, axis=flip_axis)


def parse_image_tiles(tile_data):
    tile_data_list = tile_data.split('\n\n')
    tiles = {}

    for td in tile_data_list:
        lines = td.split('\n')
        if lines[0].strip():
            tile_id = int(lines[0].replace(':', '').replace('Tile ', ''))
            lines = lines[1:]
            image = []

            for line in lines:
                row = []
                for c in line:
                    row.append(c)
                image.append(row)
        
            tiles[tile_id] = image

    return tiles


def stitch(tiles):
    linked_array = {tile_id: [None, None, None, None] for tile_id in tiles}  # stores neighbors to the NESW, -1 for no neighbor
    current_tile = tiles.keys()[0]
    reoriented_tiles = {current_tile: tiles[current_tile]}

    while True:
        pass
        # Find all neighbors for current tile
        #   If candidate tiles have already had orientation fixed, do not allow changing orientation
        #   If candidate tiles already have a match on the matching face, skip them

        # Next current tile will be a tile that has been reoriented and has open neighbors (some None in linked array)
        # Continue until all tiles have all neighbors found

    return linked_array, reoriented_tiles


sample_tiles = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

'''

image_tiles = parse_image_tiles(sample_tiles)
image = image_tiles[3079]
vert_flipped = flip(image)
horz_flipped = flip(image, axis=1)
cw_rotated = rotate(image)
ccw_rotated = rotate(image, direction='CCW')

display(image, 'Original')
display(vert_flipped, 'Flip Vertically')
display(horz_flipped, 'Flip Horizontally')
display(cw_rotated, 'CW Rotation')
display(ccw_rotated, 'CCW Rotation')

print('Done!')
