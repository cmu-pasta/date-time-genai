
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def time_to_seconds_since_midnight(t: time) -> float:
    # Step 1: Extract time components
    hours = t.hour
    minutes = t.minute
    seconds = t.second
    microseconds = t.microsecond
    
    # Step 2: Convert all components to seconds
    total_seconds = (hours * 3600) + (minutes * 60) + seconds + (microseconds / 1000000)
    
    # Step 3: Return the result
    return total_seconds

# Entry point: time_to_seconds_since_midnight(t: time) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_40_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_time_to_seconds_since_midnight(t):
    result = time_to_seconds_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
