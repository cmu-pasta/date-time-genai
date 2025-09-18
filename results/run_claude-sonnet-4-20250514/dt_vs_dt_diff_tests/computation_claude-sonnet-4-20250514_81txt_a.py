
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def calculate_milliseconds_in_duration(duration: timedelta) -> int:
    # Step 1: Get total seconds from the timedelta
    total_seconds = duration.total_seconds()
    
    # Step 2: Convert seconds to milliseconds (multiply by 1000)
    total_milliseconds = total_seconds * 1000
    
    # Step 3: Return as integer
    return int(total_milliseconds)

# Entry point: calculate_milliseconds_in_duration(duration: timedelta) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_81txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_calculate_milliseconds_in_duration(duration):
    result = calculate_milliseconds_in_duration(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
