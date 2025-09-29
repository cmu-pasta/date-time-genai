
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def check_date_ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    # Step 1: Check if the ranges overlap using the overlap condition
    # Two ranges overlap if: start1 < end2 AND start2 < end1
    overlap = start1 < end2 and start2 < end1
    
    # Step 2: Return the boolean result
    return overlap

# Entry point: check_date_ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_25_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_check_date_ranges_overlap(start1, end1, start2, end2):
    result = check_date_ranges_overlap(start1, end1, start2, end2)
    formatted_result = format_value_dt(result, start1, end1, start2, end2)
    log_file.write(formatted_result + "\n")
