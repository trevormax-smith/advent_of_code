def read_input(day_num):
    with open('./inputs/day{:>02}.txt'.format(day_num), 'r') as f:
        contents = f.read()
    return contents

def read_input_lines(day_num):
    contents = read_input(day_num)
    return [c for c in contents.split('\n') if c.strip()]
