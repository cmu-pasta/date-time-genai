
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def calculate_time_since_epoch(timestamp: datetime) -> timedelta:
    # Step 1: Define the epoch as January 1, 1970, 00:00:00 UTC
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    
    # Step 2: Ensure the input timestamp has timezone info (assume UTC if none)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    # Step 3: Calculate the time elapsed since epoch
    time_elapsed = timestamp - epoch
    
    # Step 4: Return the timedelta
    return time_elapsed

# Entry point: calculate_time_since_epoch(timestamp: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_30_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_time_since_epoch(timestamp):
    result = calculate_time_since_epoch(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
