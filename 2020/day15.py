# Advent of Code 2020, Day 15
# Michael Bell
# 12/15/2020
from queue import Queue


class MyQueue(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []
    def put(self, val):
        if self.full():
            self.queue = self.queue[1:]
        self.queue.append(val)
    def get(self):
        val = self.queue[0]
        self.queue = self.queue[1:]
        return val
    def full(self):
        return len(self.queue) >= self.max_size
    def diff_q(self):
        if len(self.queue) <= 1:
            return None
        else:
            return self.queue[-1] - self.queue[-2]



def memory_game_result(starting_numbers, nth_number=2020):
    # Keyed on number, give a list of the turns when it was spoken
    numbers_spoken = {}
    for i, sn in enumerate(starting_numbers):
        q = MyQueue(2)
        q.put(i + 1)
        numbers_spoken[sn] = q
    
    n = len(starting_numbers) + 1  # Next turn number
    last_number_spoken = starting_numbers[-1]

    while n <= nth_number:
        last_spoken_rounds = numbers_spoken[last_number_spoken]

        number_to_speak = last_spoken_rounds.diff_q()
        if number_to_speak is None:
            number_to_speak = 0

        if number_to_speak in numbers_spoken:
            numbers_spoken[number_to_speak].put(n)
        else:
            q = MyQueue(2)
            q.put(n)
            numbers_spoken[number_to_speak] = q
        
        last_number_spoken = number_to_speak
        n += 1
        
    return last_number_spoken


sample_starting_numbers = [0,3,6]
assert memory_game_result(sample_starting_numbers) == 436
# assert memory_game_result(sample_starting_numbers, 30000000) == 175594
sample_starting_numbers = [1,3,2]
assert memory_game_result(sample_starting_numbers) == 1
# assert memory_game_result(sample_starting_numbers, 30000000) == 2578
sample_starting_numbers = [2,1,3]
assert memory_game_result(sample_starting_numbers) == 10
# assert memory_game_result(sample_starting_numbers, 30000000) == 3544142
sample_starting_numbers = [1,2,3]
assert memory_game_result(sample_starting_numbers) == 27
# assert memory_game_result(sample_starting_numbers, 30000000) == 261214
sample_starting_numbers = [2,3,1]
assert memory_game_result(sample_starting_numbers) == 78
# assert memory_game_result(sample_starting_numbers, 30000000) == 6895259
sample_starting_numbers = [3,2,1]
assert memory_game_result(sample_starting_numbers) == 438
# assert memory_game_result(sample_starting_numbers, 30000000) == 18
sample_starting_numbers = [3,1,2]
assert memory_game_result(sample_starting_numbers) == 1836
# assert memory_game_result(sample_starting_numbers, 30000000) == 362

starting_numbers = [5,2,8,16,18,0,1]
print('Part 1:', memory_game_result(starting_numbers))
print('Part 2:', memory_game_result(starting_numbers, 30000000))
