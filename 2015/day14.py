# Advent of Code 2015, Day 14
# Michael Bell
# 1/11/2021
import helper


class Reindeer(object):
    FLYING = 1
    RESTING = 0

    def __init__(self, name, speed, flying_time, resting_time):
        self.name = name
        self.speed = speed
        self.flying_time = flying_time
        self.resting_time = resting_time
        self.restart()
    
    def restart(self):
        self.distance = 0
        self.state_duration = 0
        self.current_state = Reindeer.FLYING

    def change_state(self):
        if self.current_state == Reindeer.FLYING:
            self.current_state = Reindeer.RESTING
        else:
            self.current_state = Reindeer.FLYING
        self.state_duration = 0

    def remaining_time_in_state(self):
        if self.current_state == Reindeer.FLYING:
            return self.flying_time - self.state_duration
        else:
            return self.resting_time - self.state_duration

    def advance_if_flying(self, n_steps):
        if self.current_state == Reindeer.FLYING:
            self.distance += n_steps * self.speed

    def race(self, n_steps=1):

        time_left_in_current_state = self.remaining_time_in_state()

        if n_steps < time_left_in_current_state:
            self.state_duration += n_steps
            self.advance_if_flying(n_steps)
            
        else:
            self.advance_if_flying(time_left_in_current_state)
            self.change_state()

            remaining_steps = n_steps - time_left_in_current_state
            self.race(remaining_steps)


def parse_reindeer(reindeer_specs):
    reindeer = []
    for line in reindeer_specs:
        tokens = line.replace(',', '').replace('.', '').split(' ')
        name = tokens[0]
        speed = int(tokens[3])
        flying_time = int(tokens[6])
        resting_time = int(tokens[-2])
        reindeer.append(Reindeer(name, speed, flying_time, resting_time))
    return reindeer


def race_all(reindeer, n_steps):
    for r in reindeer:
        r.race(n_steps)
    return max(reindeer, key=lambda x: x.distance)


def restart_all(reindeer):
    for r in reindeer:
        r.restart()


def new_scoring(reindeer, n_steps):
    scores = {r.name: 0 for r in reindeer}
    for _ in range(n_steps):
        race_all(reindeer, 1)
        max_dist = max(reindeer, key=lambda x: x.distance).distance
        leading_reindeer = [r for r in reindeer if r.distance == max_dist]
        for lr in leading_reindeer:
            scores[lr.name] += 1
    leader = max(scores, key=lambda x: scores[x])
    return leader, scores[leader]
    

example_reindeer_specs = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''.split('\n')

reindeer = parse_reindeer(example_reindeer_specs)
winner = race_all(reindeer, 1000)
assert winner.name == 'Comet' and winner.distance == 1120
restart_all(reindeer)
winner, winning_score = new_scoring(reindeer, 1000)
assert winner == 'Dancer' and winning_score == 689

reindeer_specs = helper.read_input_lines(14)
reindeer = parse_reindeer(reindeer_specs)
winner = race_all(reindeer, 2503)
print('Part 1:', winner.name, winner.distance)
restart_all(reindeer)
winner, winning_score = new_scoring(reindeer, 2503)
print('Part 2:', winner, winning_score)
