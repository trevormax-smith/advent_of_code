# Advent of Code 2020, Day 13
# Michael Bell
# 12/13/2020

import helper


def parse_bus_schedule(bus_schedule):
    return [int(b) if b != 'x' else None for b in bus_schedule.split(',')]


def find_next_bus(schedule, departure_time):
    next_departure_times = []
    for dp in schedule:
        if not dp:
            next_departure_times.append(None)
            continue
        n_periods = departure_time / dp
        if n_periods != int(n_periods):
            n_periods += 1
        n_periods = int(n_periods)
        next_departure_times.append(n_periods * dp)
    next_bus = min(
        [(bus_id, next_departure_time) for bus_id, next_departure_time in zip(schedule, next_departure_times) if bus_id],
        key=lambda x: x[1]
    )
    
    return next_bus[0] * (next_bus[1] - departure_time)


def next_bus(bus_routes, i):
    for j in range(i+1, len(bus_routes)):
        if bus_routes[j] is not None:
            return j
    return None


def get_repeat_period(bus_routes):
    per = 1
    for br in bus_routes:
        if br is not None:
            per *= br
    return per


def check_t(bus_routes, t):
    return all((t + i) % bs == 0 for i, bs in enumerate(bus_routes) if bs is not None)


def solve_it(bus_routes):
    next_bus_index = next_bus(bus_routes, 0)
    subset_of_busses = bus_routes[:(next_bus_index + 1)]
    current_offset = brute_force(subset_of_busses)
    current_period = get_repeat_period(subset_of_busses)

    while True:
        next_bus_index = next_bus(bus_routes, next_bus_index)
        if next_bus_index is None:
            break
        subset_of_busses = bus_routes[:(next_bus_index + 1)]
        n = 1
        while True:
            t = current_offset + n * current_period
            if check_t(subset_of_busses, t):
                new_period = get_repeat_period(subset_of_busses)
                new_offset = t
                while new_offset > 0:  # I don't think this is needed, but it doesn't really hurt
                    new_offset -= new_period
                new_offset += new_period
                current_period = new_period
                current_offset = new_offset
                break
            else:
                n += 1
        
    return current_offset


def brute_force(bus_routes):
    n = 0  # multiples of the first 

    first_route = bus_routes[0]

    while True:
        found_it = True
        for i, dp in enumerate(bus_routes):
            if not dp:
                continue
            elif (first_route * n + i) % dp != 0:
                n += 1
                found_it = False
                break
        if found_it:
            break
    
    return first_route * n


sample_arrival_time = 939
sample_bus_schedule = parse_bus_schedule('7,13,x,x,59,x,31,19')
assert find_next_bus(sample_bus_schedule, sample_arrival_time) == 295
assert brute_force(sample_bus_schedule) == 1068781
assert solve_it(sample_bus_schedule) == 1068781

sample_bus_schedule = parse_bus_schedule('17,x,13,19')
assert brute_force(sample_bus_schedule) == 3417
assert solve_it(sample_bus_schedule) == 3417

sample_bus_schedule = parse_bus_schedule('67,7,59,61')
assert brute_force(sample_bus_schedule) == 754018
assert solve_it(sample_bus_schedule) == 754018

sample_bus_schedule = parse_bus_schedule('67,x,7,59,61')
assert brute_force(sample_bus_schedule) == 779210
assert solve_it(sample_bus_schedule) == 779210
sample_bus_schedule = parse_bus_schedule('67,7,x,59,61')
assert brute_force(sample_bus_schedule) == 1261476
assert solve_it(sample_bus_schedule) == 1261476
sample_bus_schedule = parse_bus_schedule('1789,37,47,1889')
assert brute_force(sample_bus_schedule) == 1202161486
assert solve_it(sample_bus_schedule) == 1202161486


arrival_time, bus_schedule = helper.read_input_lines(13)
arrival_time = int(arrival_time)
bus_schedule = parse_bus_schedule(bus_schedule)
print('Part 1:', find_next_bus(bus_schedule, arrival_time))
print('Part 2:', solve_it(bus_schedule))
