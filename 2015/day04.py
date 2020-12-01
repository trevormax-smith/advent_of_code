# Advent of Code, 2015
# Day 4
# 11/30/2020
from hashlib import md5

def miner(secret_key, n):

    val = 1

    while True:
        md5hash = md5((secret_key + str(val)).encode('utf-8')).hexdigest()

        if md5hash[:n] == '0'*n:
            break
        
        val += 1
    
    return val

puzzle_input = 'bgvyzdsv'

# Starts w/ 5 zeros
val = miner(puzzle_input, 5)
print(val)

# Starts w/ 6 zeros
val = miner(puzzle_input, 6)
print(val)
