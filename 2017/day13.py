"""
Code for the 2017 Advent Of Code, day 13
https://adventofcode.com/2017/day/13
Michael Bell
12/17/2017
Solutions passed
"""

from collections import defaultdict
from itertools import count


def parse_layers(layers):
    layers = layers.replace('\r', '').split('\n')
    layer_list = defaultdict(int)

    for layer in layers:
        layer_depth = layer.split(': ')[0]
        layer_range = layer.split(': ')[1]

        layer_list[int(layer_depth)] = int(layer_range)
    
    return layer_list


class FirewallLayer(object):
    def __init__(self, layer_range, scanner_position=0, direction=1):
        self.scanner_position = scanner_position
        self.layer_range = layer_range
        self.direction = direction
    def increment_position(self):
        if self.direction > 0 and self.scanner_position >= self.layer_range - 1:
            self.direction = -1
        elif self.direction < 0 and self.scanner_position <= 0:
            self.direction = 1
        self.scanner_position += self.direction


class Firewall(object):
    def __init__(self, layer_def):
        if isinstance(layer_def, str):
            layer_def = parse_layers(layer_def)

            self.layers = []

            for i in range(max(layer_def.keys()) + 1):
                self.layers.append(FirewallLayer(layer_def[i]))
        else:
            self.layers = layer_def

        self.scanner_steps = 0
    
    def increment_time(self):
        self.scanner_steps += 1
        for layer in self.layers:
            layer.increment_position()

    def copy(self):
        layer_copies = [
            FirewallLayer(
                layer.layer_range, layer.scanner_position, layer.direction
            ) for layer in self.layers
        ]
        return Firewall(layer_copies)


def default_score(pos, rng):
    return pos * rng


def hit_test(pos, rng):
    if rng > 0:
        return 1
    else:
        return 0


def score_run(firewall_layers, delay=0, score_function=None, break_when_hit=False):

    if isinstance(firewall_layers, Firewall):
        firewall = firewall_layers
    else:
        firewall = Firewall(firewall_layers)

    if score_function is None:
        score_function = default_score

    packet_position = -delay - 1
    score = 0

    while packet_position < len(firewall.layers) - 1:
        packet_position += 1

        if packet_position >= 0:
            layer = firewall.layers[packet_position]
        else:
            layer = None
        
        if layer is not None and layer.scanner_position == 0 and layer.layer_range > 0:
            score += score_function(packet_position, layer.layer_range)
            if break_when_hit:
                break
        
        firewall.increment_time()

    return score


def find_delay(firewall_layers):

    firewall = Firewall(firewall_layers)

    for delay in count():

        if score_run(firewall.copy(), score_function=hit_test, break_when_hit=True) == 0:
            break

        firewall.increment_time()

        if (delay + 1) % 10000 == 0:
            print(delay + 1)

    return delay


TEST_INPUT = """0: 3
1: 2
4: 4
6: 4"""

with open('data/day13_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':
    assert score_run(TEST_INPUT) == 24
    assert score_run(TEST_INPUT, 10) == 0
    test_firewall = Firewall(TEST_INPUT)
    for _ in range(10):
        test_firewall.increment_time()
    assert score_run(test_firewall) == 0
    assert find_delay(TEST_INPUT) == 10
    print('All tests passed!')
    print('Solution 1: {:}'.format(score_run(PUZZLE_INPUT)))
    print('Solution 2: {:}'.format(find_delay(PUZZLE_INPUT)))
