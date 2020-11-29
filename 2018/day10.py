# Code for the 2018 AoC, day 10
# https://adventofcode.com/2018/day/10
# Michael Bell
# 12/10/2018
import sys


def parse_point_spec(point_spec):

    lines = point_spec.split('\n')
    pos = []
    vel = []
    for line in lines:

        x, y = tuple(int(coord) for coord in line[line.find('<')+1:line.find('>')].split(','))
        vx, vy = tuple(int(coord) for coord in line[line.find('velocity')+10:-1].split(','))

        pos.append((x, y))
        vel.append((vx, vy))

    return pos, vel 


def propagate(pos, vel, dt=1):

    new_pos = []

    for xy, vxvy in zip(pos, vel):
        new_pos.append((xy[0] + dt * vxvy[0], xy[1] + dt * vxvy[1]))
    
    return new_pos


def get_dims(pos):
    x_max = max(pos, key=lambda x: x[0])[0]
    x_min = min(pos, key=lambda x: x[0])[0]
    y_max = max(pos, key=lambda x: x[1])[1]
    y_min = min(pos, key=lambda x: x[1])[1]

    nx = x_max - x_min + 1
    ny = y_max - y_min + 1

    return x_min, nx, y_min, ny


def print_points(pos):

    x_min, nx, y_min, ny = get_dims(pos)

    grid = [['.' for i in range(nx)] for j in range(ny)]

    for xy in pos:
        grid[xy[1] - y_min][xy[0] - x_min] = '#'

    for row in grid:
        print(''.join(row))


def find_message(pos, vel):

    min_y_extent = sys.maxsize
    current_pos = pos
    t = 0

    while True:

        next_pos = propagate(current_pos, vel)
        x_min, nx, y_min, ny = get_dims(next_pos)
        
        if ny <= min_y_extent:
            min_y_extent = ny
            current_pos = next_pos
            t += 1
        else:
            print(f"Message found after {t} seconds")
            print_points(current_pos)
            break


if __name__ == '__main__':

    test_input = '''position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>'''

    test_x, test_v = parse_point_spec(test_input)

    test_x_f = propagate(test_x, test_v, 3)

    find_message(test_x, test_v)
    print()

    with open('./data/day10_input.txt', 'r') as f:
        input1 = f.read()

    x, v = parse_point_spec(input1)

    find_message(x, v)
