
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def check_date_ranges_overlap(start1: date, end1: date, start2: date, end2: date) -> bool:
    # Step 1: Check if the ranges overlap using the overlap condition
    # Two ranges overlap if: max(start1, start2) <= min(end1, end2)
    overlap = max(start1, start2) <= min(end1, end2)
    
    # Step 2: Return the boolean result
    return overlap

# Entry point: check_date_ranges_overlap(start1: date, end1: date, start2: date, end2: date) -> bool

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_25txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy(), date_strategy(), date_strategy())
def test_check_date_ranges_overlap(start1, end1, start2, end2):
    result = check_date_ranges_overlap(start1, end1, start2, end2)
    formatted_result = format_value_dt(result, start1, end1, start2, end2)
    log_file.write(formatted_result + "\n")
