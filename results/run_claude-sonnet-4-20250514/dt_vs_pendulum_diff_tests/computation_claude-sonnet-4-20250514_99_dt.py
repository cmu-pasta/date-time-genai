
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def calculate_decimal_time(t: time) -> float:
    # Step 1: Extract hours, minutes, seconds, and microseconds from the time object
    hours = t.hour
    minutes = t.minute
    seconds = t.second
    microseconds = t.microsecond
    
    # Step 2: Calculate total seconds since midnight
    total_seconds = hours * 3600 + minutes * 60 + seconds + microseconds / 1000000
    
    # Step 3: Convert to decimal time (fraction of a day)
    # Total seconds in a day = 24 * 60 * 60 = 86400
    decimal_time = total_seconds / 86400
    
    # Step 4: Return the decimal representation
    return decimal_time

# Entry point: calculate_decimal_time(t: time) -> float

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_99_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_calculate_decimal_time(t):
    result = calculate_decimal_time(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
