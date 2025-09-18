
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_weekend_days_between(start: date, end: date) -> int:
    """
    Calculate the number of weekend days (Saturdays and Sundays) between two dates, inclusive.
    Inputs:
      - start: date
      - end: date
    Output:
      - integer count of weekend days within the inclusive range [start, end]
    """
    # Ensure start <= end
    if start > end:
        start, end = end, start

    # Total days inclusive
    total_days = (end - start).days + 1

    # Number of complete weeks and base weekend days from those weeks
    full_weeks = total_days // 7
    weekend_days = full_weeks * 2

    # Remaining days after full weeks
    remaining_days = total_days % 7
    start_wd = start.weekday()  # Monday=0, Sunday=6

    # Count weekend days within the remaining span
    for i in range(remaining_days):
        wd = (start_wd + i) % 7
        if wd == 5 or wd == 6:  # Saturday or Sunday
            weekend_days += 1

    return int(weekend_days)

# Entry point: count_weekend_days_between(start: date, end: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_15txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_weekend_days_between(start, end):
    result = count_weekend_days_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
