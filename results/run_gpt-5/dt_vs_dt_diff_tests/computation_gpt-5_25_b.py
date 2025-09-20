
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    # Normalize the first range
    if end1 < start1:
        s1 = end1
        e1 = start1
    else:
        s1 = start1
        e1 = end1

    # Normalize the second range
    if end2 < start2:
        s2 = end2
        e2 = start2
    else:
        s2 = start2
        e2 = end2

    # Ranges overlap if they are not strictly disjoint
    return not (e1 < s2 or e2 < s1)

# Entry point: ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_25_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_ranges_overlap(start1, end1, start2, end2):
    result = ranges_overlap(start1, end1, start2, end2)
    formatted_result = format_value_dt(result, start1, end1, start2, end2)
    log_file.write(formatted_result + "\n")
