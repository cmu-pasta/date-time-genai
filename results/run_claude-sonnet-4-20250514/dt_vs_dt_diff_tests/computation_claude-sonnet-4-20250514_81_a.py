
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def calculate_milliseconds(duration: timedelta) -> int:
    # Step 1: Get the total duration in seconds as a float
    total_seconds = duration.total_seconds()
    
    # Step 2: Convert seconds to milliseconds by multiplying by 1000
    milliseconds = total_seconds * 1000
    
    # Step 3: Convert to integer and return
    return int(milliseconds)

# Entry point: calculate_milliseconds(duration: timedelta) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_81_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_calculate_milliseconds(duration):
    result = calculate_milliseconds(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
