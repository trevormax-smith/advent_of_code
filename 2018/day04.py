# Code for the 2018 AoC, day 4
# https://adventofcode.com/2018/day/4
# Michael Bell
# 12/4/2018

from datetime import datetime
from collections import defaultdict


def get_time_and_message(activity_record):
    rp = activity_record.split(']')
    ts = rp[0].replace('[', '')
    dt = datetime.strptime(ts, '%Y-%m-%d %H:%M') 
    return (dt, rp[1].strip())
    

def parse_activity_log(activity_log):
    """
    Parse a string of lines containing an activity log into a set of "shift logs" which include
    the guard ID, start time, and a list of times when the guard fell asleep/woke up.
    """

    times_and_messages = sorted(
        [get_time_and_message(al) for al in activity_log.split('\n')], 
        key=lambda x: x[0]
    )

    shift_logs = []
    current_log = dict()
    for tm in times_and_messages:
        if 'begins' in tm[1]:
            if len(current_log) > 0:
                shift_logs.append(current_log)
            current_log = {
                'id': int(tm[1].split()[1].replace('#', '')),
                'shift_start': tm[0],
                'sleep_times': [],
                'wake_times': []
            }
        elif 'falls' in tm[1]:
            current_log['sleep_times'].append(tm[0])
        elif 'wakes' in tm[1]:
            current_log['wake_times'].append(tm[0])
    
    shift_logs.append(current_log)
    
    return shift_logs


def dict_keymax(d):
    """
    Given a dictionary of arbitrary keys and integer values >= 0, return the key of the max
    item with the max value.
    """
    max_k = -1
    max_v = -1
    for k in d:
        v = d[k]
        if v > max_v:
            max_v = v
            max_k = k
    return max_k


def get_sleepiest_guard(shift_logs):
    """
    Get the ID of the guard who has slept the most over all shifts.
    """

    # Index on guard ID and tally up total time asleep over all observed shifts
    sleep_tallies = defaultdict(int)

    # Iterate over shifts to compute time asleep and assign to the guard's total
    for shift_log in shift_logs:
        sleep_time = 0
        for st, wt in zip(shift_log['sleep_times'], shift_log['wake_times']):
            sleep_time += int((wt - st).total_seconds() / 60)
        sleep_tallies[shift_log['id']] += sleep_time

    max_id = dict_keymax(sleep_tallies)

    return max_id


def get_most_likely_sleep_time(guard_id, shift_logs):
    """
    Find the time when a given guard is most likely asleep.
    """

    guard_logs = [shift_log for shift_log in shift_logs if shift_log['id'] == guard_id]

    sleep_counts = defaultdict(int)

    for guard_log in guard_logs:
        sleep_intervals = list(zip(guard_log['sleep_times'], guard_log['wake_times']))
        for i in range(60):
            if any(st.minute <= i < wt.minute for st, wt in sleep_intervals):
                sleep_counts[i] += 1

    max_index = dict_keymax(sleep_counts)
    return max_index


def strategy1(shift_logs):
    """
    Find the guard who is most often asleep overall. Return their ID and the time when they are
    most often asleep.
    """
    
    guard_id = get_sleepiest_guard(shift_logs)
    mlst = get_most_likely_sleep_time(guard_id, shift_logs)
    return guard_id, mlst


def strategy2(shift_logs):
    """
    Find the guard who is most often asleep at a given time. Return guard id and time when they 
    are most often asleep.
    """

    guard_sleep_counts = defaultdict(int)

    for shift_log in shift_logs: 
        guard_id = shift_log['id']
        sleep_intervals = list(zip(shift_log['sleep_times'], shift_log['wake_times']))
        for i in range(60):
            if any(st.minute <= i < wt.minute for st, wt in sleep_intervals):
                guard_sleep_counts[(guard_id, i)] += 1

    max_guard_id, max_minute = dict_keymax(guard_sleep_counts)

    return max_guard_id, max_minute


if __name__ == '__main__':
    test1 = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''

    tmp = parse_activity_log(test1)
    print(strategy1(tmp))
    assert strategy1(tmp)[0] == 10 and strategy1(tmp)[1] == 24
    assert strategy2(tmp)[0] == 99 and strategy2(tmp)[1] == 45

    with open('./data/day04_input.txt', 'r') as f:
        input1 = f.read()

    shift_logs = parse_activity_log(input1)
    guard_id, max_minute = strategy1(shift_logs)
    print(f"Solution 1: {guard_id} @ {max_minute} ({guard_id * max_minute})")

    guard_id, max_minute = strategy2(shift_logs)
    print(f"Solution 2: {guard_id} @ {max_minute} ({guard_id * max_minute})")