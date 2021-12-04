from typing import Tuple, List, Union
from helper import read_input


class BingoBoard(object):
    def __init__(self, board: str) -> None:
        # For Scott
        self.board = [[int(val) for val in row.strip().split(' ') if val != ''] for row in board.split('\n') if row.strip() != '']
        self.markings: List[List[bool]]
        self.last_number_called: Union[None, int]
        self.clear()

    def mark_number(self, number: int) -> None:
        for row_num, row in enumerate(self.board):
            for col_num, val in enumerate(row):
                if val == number:
                    self.markings[row_num][col_num] = True
        self.last_number_called = number
    
    def check_for_victory(self) -> bool:
        for row in self.markings:
            if all(row):
                return True

        for col_num in range(len(self.markings[0])):
            col = [self.markings[row_num][col_num] for row_num in range(len(self.markings))]
            if all(col):
                return True

        return False

    def score(self) -> int:
        score = 0
        if self.check_for_victory():
            for row_num, row in enumerate(self.markings):
                for col_num, col in enumerate(row):
                    if col == 0:
                        score += self.board[row_num][col_num]
            score *= self.last_number_called
        return score
    
    def clear(self) -> None:
        # A grid that has dimensions of the board itself to track which cells have been marked
        self.markings = [[False] * len(self.board[0]) for _ in range(len(self.board))]
        self.last_number_called = None


def parse_raw_input(raw_input: str) -> Tuple[List[int], List[BingoBoard]]:
    called_numbers, *raw_boards = raw_input.split('\n\n')
    called_numbers = [int(cn) for cn in called_numbers.split(',')]
    boards = [BingoBoard(board) for board in raw_boards]
    return called_numbers, boards


def find_winning_board(calls: List[int], boards: List[BingoBoard]) -> Union[BingoBoard, None]:
    for this_call in calls:
        for board in boards:
            board.mark_number(this_call)
            if board.score() > 0:
                return board
    return None


def find_losing_board(calls: List[int], boards: List[BingoBoard]) -> Union[BingoBoard, None]:
    remaining_boards = boards.copy()
    winning_boards = []
    for this_call in calls:
        next_remaining_boards = []
        for board in remaining_boards:
            board.mark_number(this_call)
            if board.score() == 0:
                next_remaining_boards.append(board)
            else:
                winning_boards.append(board)
        remaining_boards = next_remaining_boards.copy()
    return winning_boards[-1] if len(winning_boards) > 0 else None


### TESTS
test_raw_input = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

test_calls, test_boards = parse_raw_input(test_raw_input)
assert find_winning_board(test_calls, test_boards).score() == 4512
assert find_losing_board(test_calls, test_boards).score() == 1924

### THE REAL THING
raw_input = read_input(4)
calls, boards = parse_raw_input(raw_input)
winning_board = find_winning_board(calls, boards)
losing_board = find_losing_board(calls, boards)
print(f"Part 1: {winning_board.score()}")
print(f"Part 2: {losing_board.score()}")
