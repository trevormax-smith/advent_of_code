from dataclasses import dataclass
from typing import List
from helper import read_input_lines


@dataclass
class Submarine(object):
    """Keep track of the position of the submarine using basic cartesian logic"""
    horizontal: int = 0
    depth: int = 0

    def move(self, command: str) -> None:
        match command.split():
            case ["down", steps]:
                self.depth += int(steps)
            case ["up", steps]:
                self.depth -= int(steps)
            case ["forward", steps]:
                self.horizontal += int(steps)
            case _:
                raise Exception("Improper command: {command}")
    
    def get_position_hash(self) -> int:
        return self.horizontal * self.depth

    def chart_course(self, course: List[str]) -> None:
        for command in course:
            self.move(command)


@dataclass
class AimedSubmarine(Submarine):
    """Keep track of position of the submarine using Aim and Move logic"""
    aim: int = 0

    def move(self, command: str) -> None:
        match command.split():
            case ["down", steps]:
                self.aim += int(steps)
            case ["up", steps]:
                self.aim -= int(steps)
            case ["forward", steps]:
                self.horizontal += int(steps)
                self.depth += int(steps) * self.aim
            case _:
                raise Exception("Improper command: {command}")


test_course = """forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip().split('\n')

test_position = Submarine()
test_position.chart_course(test_course)
assert test_position.horizontal == 15
assert test_position.depth == 10
assert test_position.get_position_hash() == 150

test_position = AimedSubmarine()
test_position.chart_course(test_course)
assert test_position.horizontal == 15
assert test_position.depth == 60
assert test_position.get_position_hash() == 900

course = read_input_lines(2)
position = Submarine()
position.chart_course(course)
print(f'Part 1: {position.get_position_hash()}')

second_position = AimedSubmarine()
second_position.chart_course(course)
print(f'Part 2: {second_position.get_position_hash()}')
