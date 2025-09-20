
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_timezone_difference(dt1: datetime, dt2: datetime) -> timedelta:
    # Step 1: Calculate the difference between timezone-aware datetime objects
    # Python automatically handles timezone conversion when subtracting datetime objects
    difference = dt2 - dt1
    
    # Step 2: Return the timedelta result
    return difference

# Entry point: calculate_timezone_difference(dt1: datetime, dt2: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_69_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_timezone_difference(dt1, dt2):
    result = calculate_timezone_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
