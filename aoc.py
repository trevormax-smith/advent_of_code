'''
CLI for AOC
'''
import datetime
from urllib import request
import argparse
import os, sys
base_path = os.path.dirname(os.path.abspath(__file__))

cookie = os.environ.get('AOC_COOKIE')

def get_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5), 'EST'))


def valid_date(year: int, day: int) -> bool:
    today = get_today()
    return (2015 <= year <= today.year) and (
            (year < today.year) or 
        (today.month == 12 and day <= today.day)
    )


def download_puzzle_input(year: int, day: int) -> str:
   
    input_url = f'https://adventofcode.com/{year}/day/{day}/input'
    filepath = os.path.join(base_path, f'./{year}/inputs/day{day:>02}.txt') 

    if os.path.exists(filepath):
        raise FileExistsError(f'Input file {filepath} already exists.')
    
    hdr = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Cookie': cookie
    }

    req = request.Request(input_url, headers=hdr)
    with request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    if 'Please log in' in html:
        raise PermissionError('Must be logged in at https://adventofcode.com to use the aoc cli.')
    elif '404 Not Found' in html:
        raise FileNotFoundError(f'Input not found for {input_url}.')

    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, 'x') as f:
        f.write(html)

    return filepath


def create_py_file_template(year: int, day: int) -> str:
    with open(os.path.join(base_path, 'pyfile.template'), 'r') as f:
        file_template = f.read()

    filepath = os.path.join(base_path, f'./{year}/day{day:>02}.py')
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    
    with open(filepath, 'x') as f:
        f.write(file_template)
    return filepath


if __name__ == '__main__':
    
    today = get_today()
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')
    parser_init = subparsers.add_parser('init', help='Initialize AoC files for the given day (defaults to today).')
    parser_init.add_argument('-d', '--day', type=int, default=today.day)
    parser_init.add_argument('-y', '--year', type=int, default=today.year)

    init_args = parser.parse_args()

    if init_args.subparser_name == 'init':    
        year = init_args.year
        day = init_args.day

        if not valid_date(year, day):
            print(f'There is not a puzzle for the date {year}-12-{day:>02}.')
        elif cookie is None:
            print(f'You must set the AOC_COOKIE environment variable to continue')
        else:
            print(f'Initializing input and python files for AoC {year}, day {day}...')

            try:
                puzzle_input_path = download_puzzle_input(year, day)
            except FileExistsError:
                print(f'    Input file already exists! If you want to redownload the input file, please delete the existing file in ./{year}/inputs/day{day:>02}.txt')
            except PermissionError:
                print(f'    You are not logged into AoC. Please log in at https://adventofcode.com to download input files.')
            else:
                print(f'    Puzzle input written to {puzzle_input_path}')

            try:
                pyfile_input_path = create_py_file_template(year, day)
            except FileExistsError:
                print(f'    Template .py file already exists in ./{year}/day{day:>02}.py')
            else:
                print(f'    Template .py file written to {puzzle_input_path}')
