# Advent of Code 2020, Day 02
# Michael Bell
# 12/2/2020


def parse_password_db(password_list):
    records = [r for r in password_list.split('\n') if r.strip()]

    pw_db = []

    for record in records:
        policy_def, pw = record.split(':')  # throws error if more than two things result
        pw = pw.strip()
        min_max_def, letter = policy_def.split()
        min_n, max_n = min_max_def.split('-')

        pw_db.append({
            'pw': pw,
            'required_letter': letter,
            'min_required': int(min_n),
            'max_required': int(max_n)
        })

    return pw_db


def is_pw_valid_sled(pw_db_record):

    pw = pw_db_record['pw']
    req_letter = pw_db_record['required_letter']
    min_n = pw_db_record['min_required']
    max_n = pw_db_record['max_required']

    n = pw.count(req_letter)

    if min_n <= n <= max_n:
        return True

    return False


def is_pw_valid_toboggan(pw_db_record):

    pw = pw_db_record['pw']
    req_letter = pw_db_record['required_letter']
    min_n = pw_db_record['min_required']
    max_n = pw_db_record['max_required']

    check_char_1 = pw[min_n-1]
    check_char_2 = pw[max_n-1]

    if (check_char_1 == req_letter or check_char_2 == req_letter) and not (check_char_1 == req_letter and check_char_2 == req_letter):
        return True

    return False


def count_valid_passwords(pw_db, check_fn=is_pw_valid_sled):

    return sum(int(check_fn(db_record)) for db_record in pw_db)


# Tests
sample_db = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''

assert count_valid_passwords(parse_password_db(sample_db)) == 2
assert count_valid_passwords(parse_password_db(sample_db), is_pw_valid_toboggan) == 1

# The real thing
with open('./inputs/day02.txt', 'r') as f:
    raw_pw_db = f.read()

pw_db = parse_password_db(raw_pw_db)

print('Part 1:', count_valid_passwords(pw_db))
print('Part 2:', count_valid_passwords(pw_db, is_pw_valid_toboggan))
