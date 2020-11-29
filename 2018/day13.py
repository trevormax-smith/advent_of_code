# Code for the 2018 AoC, day 13
# https://adventofcode.com/2018/day/13
# Michael Bell
# 12/13/2018

turn_sequence = ['left', 'straight', 'right']
directions = ['up', 'right', 'down', 'left']


class Car(object):
    def __init__(self, x, y, direction, next_turn=0):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = next_turn
    
    def move(self):
        if directions[self.direction] == 'up':
            self.y -= 1
        elif directions[self.direction] == 'down':
            self.y += 1
        elif directions[self.direction] == 'left':
            self.x -= 1
        elif directions[self.direction] == 'right':
            self.x += 1
    
    def turn(self, curve=None):

        if curve is None or curve == '+':
            if turn_sequence[self.next_turn] == 'left':
                self.direction = (self.direction - 1) % 4
            elif turn_sequence[self.next_turn] == 'right':
                self.direction = (self.direction + 1) % 4
            self.next_turn = (self.next_turn + 1) % 3
        elif curve == '\\':
            if directions[self.direction] == 'right' or directions[self.direction] == 'left':
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4
        elif curve == '/':
            if directions[self.direction] == 'right' or directions[self.direction] == 'left':
                self.direction = (self.direction - 1) % 4
            else:
                self.direction = (self.direction + 1) % 4

    def __repr__(self):
        return f'Car({self.x}, {self.y}, {directions[self.direction]}, {turn_sequence[self.next_turn]})'
    
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def map_repr(self):
        if directions[self.direction] == 'right':
            return '>'
        elif directions[self.direction] == 'left':
            return '<'
        elif directions[self.direction] == 'up':
            return '^'
        else:
            return 'v'


def parse_track_map(track_map):

    track_carts = track_map.split('\n')
    track = []
    carts = []  # Each cart def'd by x, y coord, direction, and the next turn direction

    for y, row in enumerate(track_carts):
        track_row = str(row.lower())
        for x, track_piece in enumerate(row):
            if track_piece == '<':
                carts.append(Car(x, y, 3, 0))
                track_row = track_row.replace('<', '-', 1)
            elif track_piece == '>':
                carts.append(Car(x, y, 1, 0))
                track_row = track_row.replace('>', '-', 1)
            elif track_piece == '^':
                carts.append(Car(x, y, 0, 0))
                track_row = track_row.replace('^', '|', 1)
            elif track_piece == 'V' or track_piece == 'v':
                carts.append(Car(x, y, 2, 0))
                track_row = track_row.replace('v', '|', 1)

        track.append(track_row)
    return track, carts        


def move_cars(cars, track_map, stop_at_crash=True):

    crashed_cars = []

    for car in sorted(cars, key=lambda c: (c.y, c.x)):
        car.move()
        car.turn(track_map[car.y][car.x])

        crash = check_for_crash(cars)
        if crash is not None:
            crashed_cars.extend([car for car in cars if car == crash and car not in crashed_cars])
            if stop_at_crash:
                return crash

    for car in crashed_cars:
        cars.remove(car)

    return crash
    
    
def check_for_crash(cars):

    sorted_cars = sorted(cars, key=lambda c: (c.x, c.y))
    for car1, car2 in zip(sorted_cars[:-1], sorted_cars[1:]):
        if car1 == car2:
            return car1
    return None


def go_until_crash(cars, track_map):

    cars = [car for car in cars]

    n = 0
    while True:
        # print_track_and_cars(cars, track_map)
        # _ = input('hit enter')
        # print('\n'*3)
        car_crash = move_cars(cars, track_map)
        if car_crash:
            break
        n += 1
    # print(f'Crash at step {n}')
    return car_crash


def go_until_one_car_left(cars, track_map):

    cars = [car for car in cars]

    n = 0
    while True:
        _ = move_cars(cars, track_map, False)
        if len(cars) <= 1:
            break
        n += 1

    return cars


def print_track_and_cars(cars, track):
    for y, line in enumerate(track):
        these_cars = [car for car in cars if car.y == y]

        to_print = str(line)
        for car in these_cars:
            to_print = to_print[:car.x] + car.map_repr() + to_print[(car.x + 1):]

        print(to_print)


if __name__ == '__main__':

    test_track_map = r'''/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   '''

    track, cars = parse_track_map(test_track_map)
    car_crash = go_until_crash(cars, track)

    assert car_crash.x == 7 and car_crash.y == 3

    with open('./data/day13_input.txt', 'r') as f:
        input1 = f.read()

    track, cars = parse_track_map(input1)
    car_crash = go_until_crash(cars, track)
    print(f'Solution 1: {car_crash.x},{car_crash.y}')

    remaining_cars = go_until_one_car_left(cars, track)
    print(f'Solution 2: {remaining_cars[0].x},{remaining_cars[0].y}')
