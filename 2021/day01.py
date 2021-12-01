from typing import List
import helper


def parse_raw_sonar_report(raw_sonar_report: str) -> List[int]:
    return [int(x) for x in raw_sonar_report.split('\n') if x != '']


def count_depth_increases(sonar_report: List[int]) -> int:
    return sum(1 for last_depth, depth in zip(sonar_report[:-1], sonar_report[1:]) if depth > last_depth)


def windowed_sum(sonar_report: List[int], window_length: int = 3) -> List[int]:
    windowed_report = []
    for i in range(len(sonar_report) - window_length + 1):
        windowed_report.append(
            sum(sonar_report[i:(i+window_length)])
        )
    return windowed_report


sample_sonar_report = """199
200
208
210
200
207
240
269
260
263"""

sample_sonar_report = parse_raw_sonar_report(sample_sonar_report)
assert count_depth_increases(sample_sonar_report) == 7
windowed_sample_sonar_report = windowed_sum(sample_sonar_report)
assert count_depth_increases(windowed_sample_sonar_report) == 5

raw_sonar_report = helper.read_input(1)
sonar_report = parse_raw_sonar_report(raw_sonar_report)
depth_increase_count = count_depth_increases(sonar_report)
windowed_sonar_report = windowed_sum(sonar_report)
windowed_depth_increase_count = count_depth_increases(windowed_sonar_report)
print(f"Part 1: {depth_increase_count}")
print(f"Part 2: {windowed_depth_increase_count}")
