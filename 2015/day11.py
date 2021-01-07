# Advent of Code 2015, Day 11
# Michael Bell
# 1/7/2021


def meets_requirements(pw):

    if 'i' in pw or 'o' in pw or 'l' in pw:
        return False
    
    has_straight = False
    pairs = []
    for a, b, c in zip(pw[:-2], pw[1:-1], pw[2:]):
        if (ord(c) - ord(b)) == 1 and (ord(b) - ord(a)) == 1:
            has_straight = True
        if b == a or b == c:
            pairs.append(b)
    
    if not has_straight or len(set(pairs)) < 2:
        return False

    return True


def next_pw(pw):

    next_pw = pw

    while True:

        n_chars_incremented = 1
        incremented_chars = ''
        while True:
            char_to_increment = next_pw[-n_chars_incremented]
            next_char_num = ord(char_to_increment) + 1
            if next_char_num > ord('z'):
                incremented_chars = 'a' + incremented_chars
                n_chars_incremented += 1
            else:
                incremented_chars = chr(next_char_num) + incremented_chars
                break
        
        next_pw = next_pw[:-n_chars_incremented] + incremented_chars

        if meets_requirements(next_pw):
            break
    
    return next_pw


sample_pw = 'abcdefgh'
assert next_pw(sample_pw) == 'abcdffaa'
sample_pw = 'ghijklmn'
assert next_pw(sample_pw) == 'ghjaabcc'

pw = 'vzbxkghb'
new_pw = next_pw(pw)
print('Part 1:', new_pw)
new_pw = next_pw(new_pw)
print('Part 2:', new_pw)
