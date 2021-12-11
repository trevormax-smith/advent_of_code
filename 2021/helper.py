from typing import List
import sys    
import os    


calling_file_name =  os.path.basename(sys.argv[0])
puzzle_day = int(calling_file_name.replace('day', '').replace('.py', ''))


def read_input(day_num: int=None) -> str:
    if not day_num:
        day_num = puzzle_day
    with open('./inputs/day{:>02}.txt'.format(day_num), 'r') as f:
        contents = f.read()
    return contents

def read_input_lines(day_num: int=None) -> List[str]:
    if not day_num:
        day_num = puzzle_day
    contents = read_input(day_num)
    return [c for c in contents.split('\n') if c.strip()]
