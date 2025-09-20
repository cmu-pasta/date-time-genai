
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_time_to_minutes_since_midnight(t: time) -> int:
    # Step 1: Calculate total minutes since midnight
    # Convert hours to minutes, add minutes, and add seconds converted to minutes
    total_minutes = t.hour * 60 + t.minute + t.second / 60.0
    
    # Step 2: Convert to integer (truncating any fractional minutes)
    return int(total_minutes)

# Entry point: convert_time_to_minutes_since_midnight(t: time) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_64_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_minutes_since_midnight(t):
    result = convert_time_to_minutes_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
