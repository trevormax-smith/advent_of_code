from typing import Tuple, List
from helper import read_input_lines


bracket_pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
corrupted_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
incomplete_scores = {')': 1, ']': 2, '}': 3, '>': 4}


def get_corrupted_lines(code: List[str]) -> List[Tuple[str, str]]:
    corrupted_lines = []
    for line in code:
        stack = []
        for char in line:
            if char in bracket_pairs:
                stack.append(char)
            else:
                other_char = stack.pop()
                if char != bracket_pairs[other_char]:
                    corrupted_lines.append((line, char))
    return corrupted_lines


def score_corrupted_lines(code: List[str]) -> int:
    corrupted_lines = get_corrupted_lines(code)
    score = 0
    for line, offending_char in corrupted_lines:
        score += corrupted_scores[offending_char]
    return score


def get_incomplete_lines(code: List[str]) -> List[str]:
    corrupted_lines = get_corrupted_lines(code)
    corrupted_lines = [cl[0] for cl in corrupted_lines]
    incomplete_lines = [line for line in code if line not in corrupted_lines]
    return incomplete_lines


def complete_line(line: str) -> str:
    stack = []
    for char in line:
        if char in bracket_pairs:
            stack.append(char)
        else:
            stack.pop()
    remaining_chars = []
    while stack:
        remaining_chars.append(bracket_pairs[stack.pop()])
    return line + ''.join(remaining_chars)


def line_score(complete_line: str, original_line: str) -> int:
    score = 0
    for i in range(len(original_line), len(complete_line)):
        score *= 5
        score += incomplete_scores[complete_line[i]]
    return score


def score_incomplete_lines(code: List[str]) -> int:
    incomplete_lines = get_incomplete_lines(code)
    scores = []
    for incomplete_line in incomplete_lines:
        completed_line = complete_line(incomplete_line)
        scores.append(line_score(completed_line, incomplete_line))

    return sorted(scores)[len(scores) // 2]


### TEST
test_code = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.split('\n')
assert score_corrupted_lines(test_code) == 26397
assert complete_line('[({(<(())[]>[[{[]{<()<>>') == '[({(<(())[]>[[{[]{<()<>>}}]])})]'
assert score_incomplete_lines(test_code) == 288957


### THE REAL THING
code = read_input_lines(10)
print(f'Part 1: {score_corrupted_lines(code)}')
print(f'Part 2: {score_incomplete_lines(code)}')
