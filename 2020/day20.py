# Advent of Code 2020, Day 20
# Michael Bell
# 12/20/2020

import helper


sea_monster_template = [
    [c for c in '                  # '],
    [c for c in '#    ##    ##    ###'],
    [c for c in ' #  #  #  #  #  #   '],
]


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


def get_row(image, row_num):
    return image[row_num]


def get_col(image, col_num):
    col = []
    for row in image:
        col.append(row[col_num])
    return col


def get_edge(image, direction):
    direction = direction % 4

    if direction == 0:
        return get_row(image, 0)
    elif direction == 2:
        return get_row(image, -1)
    elif direction == 1:
        return get_col(image, -1)
    elif direction == 3:
        return get_col(image, 0)


def get_opposite_edge(image, direction):
    return get_edge(image, direction + 2)


def copy(image):
    n_rows, n_cols = get_dims(image)
    new_image = init_image(n_rows, n_cols)
    for row_num in range(n_rows):
        for col_num in range(n_cols):
            new_image[row_num][col_num] = image[row_num][col_num]
    return new_image


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


def check_neighbor(ref_image, other_image, direction, reorient=True):
    # return None if not a match, otherwise return the other_image, perhaps re-oriented if allowed
    
    other_image_copy = copy(other_image)

    for _ in range(2):
        for _ in range(4):
            if get_edge(ref_image, direction) == get_opposite_edge(other_image_copy, direction):
                return other_image_copy
            if not reorient:
                return None
            other_image_copy = rotate(other_image_copy)
        other_image_copy = flip(other_image_copy)
    return None


# Need a function to turn linked array into array of image IDs
def linked_array_to_array(linked_array):
    current_id = [k for k in linked_array if linked_array[k][0] < 0 and linked_array[k][-1] < 0][0]

    array = []
    row = [current_id]
    while not (linked_array[current_id][1] < 0 and linked_array[current_id][2] < 0):
        if linked_array[current_id][1] > 0:
            # In the middle of a row
            current_id = linked_array[current_id][1]
        elif linked_array[current_id][1] < 0:
            # At end of the row, to go next row
            array.append(row)
            row = []
            last_row_first_col = array[-1][0]
            current_id = linked_array[last_row_first_col][2]
        row.append(current_id)
    array.append(row)

    return array


def image_tiles_to_image(linked_id_array, image_tiles):
    id_array = linked_array_to_array(linked_id_array)
    tile_n_rows, tile_n_cols = get_dims(image_tiles[id_array[0][0]])
    tile_n_rows -= 2
    tile_n_cols -= 2
    id_array_rows, id_array_cols = get_dims(id_array)

    # Init a blank image
    image = init_image(id_array_rows * tile_n_rows, id_array_cols * tile_n_cols)

    for id_row_num, id_row in enumerate(id_array):
        sub_image_top_row_num = id_row_num * tile_n_rows
        for id_col_num, tile_id in enumerate(id_row):
            sub_image_left_col_num = id_col_num * tile_n_cols
            tile_image = image_tiles[tile_id]

            for tile_row_num, tile_row in enumerate(tile_image[1:-1]):
                for tile_col_num, pixel in enumerate(tile_row[1:-1]):
                    image[sub_image_top_row_num + tile_row_num][sub_image_left_col_num + tile_col_num] = pixel
    
    return image
            

def stitch(tiles, starting_id=None):
    linked_array = {tile_id: [None, None, None, None] for tile_id in tiles}  # stores neighbors to the NESW, -1 for no neighbor
    if starting_id is None:
        current_tile = list(tiles.keys())[0]
    else:
        current_tile = starting_id
    reoriented_tiles = {current_tile: tiles[current_tile]}

    while True:
        # Find all neighbors for current tile
        for direction in range(4):
            if linked_array[current_tile][direction] is None:
                found_neighbor = False
                for tile_id in linked_array:
                    if tile_id == current_tile or linked_array[tile_id][(direction + 2) % 4] is not None:
                        # This is the current tile, or it already has a match for the matching side
                        continue
                    #   If candidate tiles have already had orientation fixed, do not allow changing orientation
                    if tile_id in reoriented_tiles:
                        result = check_neighbor(reoriented_tiles[current_tile], reoriented_tiles[tile_id], direction, reorient=False)
                    else:
                        result = check_neighbor(reoriented_tiles[current_tile], tiles[tile_id], direction)
                    
                    if result is not None:
                        linked_array[current_tile][direction] = tile_id
                        linked_array[tile_id][(direction + 2) % 4] = current_tile
                        reoriented_tiles[tile_id] = result
                        found_neighbor = True
                        break

                if not found_neighbor:
                    # Must be on an edge
                    linked_array[current_tile][direction] = -1


        # Next current tile will be a tile that has been reoriented and has open neighbors (some None in linked array)
        found_one = False
        for tile_id in reoriented_tiles:
            if any(linked_array[tile_id][d] is None for d in range(4)):
                current_tile = tile_id
                found_one = True
                break

        if not found_one:
            break

    return linked_array, reoriented_tiles


def get_corner_id_product(linked_array):
    prod = 1
    for tile_id in linked_array:
        if sum(1 for d in range(4) if linked_array[tile_id][d] < 0) == 2:
            prod *= tile_id
    return prod


def count_template_matches(original_image, template):

    n_rows_temp, n_cols_temp = get_dims(template)
    n_rows, n_cols = get_dims(original_image)

    image = copy(original_image)

    for _ in range(2):
        for _ in range(4):

            count = 0

            for ref_row_num in range(n_rows - n_rows_temp + 1):
                for ref_col_num in range(n_cols - n_cols_temp + 1):
                    
                    found_match = True
                    for temp_row_num in range(n_rows_temp):
                        for temp_col_num in range(n_cols_temp):
                            if template[temp_row_num][temp_col_num] == '#' and image[ref_row_num + temp_row_num][ref_col_num + temp_col_num] != '#':
                                found_match = False
                                break
                        if not found_match:
                            break
                    
                    if found_match:
                        count += 1
            
            if count > 0:
                break
            image = rotate(image)

        if count > 0:
            break
        image = flip(image)

    return count


def count_pixels_w_value(image, pixel_value):
    count = 0
    for row in image:
        for col in row:
            if col == pixel_value:
                count += 1
    return count


### TESTS ###################################################
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

# display(image, 'Original')
# display(vert_flipped, 'Flip Vertically')
# display(horz_flipped, 'Flip Horizontally')
# display(cw_rotated, 'CW Rotation')
# display(ccw_rotated, 'CCW Rotation')

linked_id_array, oriented_tiles = stitch(image_tiles, 3079)
assert get_corner_id_product(linked_id_array) == 20899048083289
stitched_image = image_tiles_to_image(linked_id_array, oriented_tiles)

# display(stitched_image)

template_matches = count_template_matches(stitched_image, sea_monster_template)
assert template_matches == 2
rough_water_in_image = count_pixels_w_value(stitched_image, '#') - template_matches * count_pixels_w_value(sea_monster_template, '#')
assert rough_water_in_image == 273

### THE REAL THING ####################################################

data = helper.read_input(20)
image_tiles = parse_image_tiles(data)
linked_id_array, oriented_tiles = stitch(image_tiles)
print('Part 1:', get_corner_id_product(linked_id_array))
stitched_image = image_tiles_to_image(linked_id_array, oriented_tiles)
template_matches = count_template_matches(stitched_image, sea_monster_template)
rough_water_in_image = count_pixels_w_value(stitched_image, '#') - template_matches * count_pixels_w_value(sea_monster_template, '#')
print('Part 2:', rough_water_in_image)