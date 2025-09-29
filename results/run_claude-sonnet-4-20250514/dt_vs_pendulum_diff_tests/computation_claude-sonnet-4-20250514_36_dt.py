
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_milliseconds_duration(timestamp1: datetime, timestamp2: datetime) -> float:
    # Step 1: Calculate the difference between the two timestamps
    time_difference = timestamp2 - timestamp1
    
    # Step 2: Convert the timedelta to total seconds and then to milliseconds
    milliseconds = time_difference.total_seconds() * 1000
    
    # Step 3: Return the absolute value to ensure positive duration
    return abs(milliseconds)

# Entry point: calculate_milliseconds_duration(timestamp1: datetime, timestamp2: datetime) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_36_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_milliseconds_duration(timestamp1, timestamp2):
    result = calculate_milliseconds_duration(timestamp1, timestamp2)
    formatted_result = format_value_dt(result, timestamp1, timestamp2)
    log_file.write(formatted_result + "\n")
