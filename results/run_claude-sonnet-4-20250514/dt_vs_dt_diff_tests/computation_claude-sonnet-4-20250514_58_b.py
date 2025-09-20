
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_unix_to_windows_epoch(unix_timestamp: float) -> float:
    # Step 1: Convert Unix timestamp to datetime object
    dt = datetime.fromtimestamp(unix_timestamp)
    
    # Step 2: Define Windows epoch start date (January 1, 1601, 00:00:00 UTC)
    windows_epoch_start = datetime(1601, 1, 1)
    
    # Step 3: Calculate the difference between the datetime and Windows epoch start
    time_difference = dt - windows_epoch_start
    
    # Step 4: Convert the difference to total seconds (Windows epoch timestamp)
    windows_timestamp = time_difference.total_seconds()
    
    # Step 5: Return the Windows epoch timestamp
    return windows_timestamp

# Entry point: convert_unix_to_windows_epoch(unix_timestamp: float) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_58_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_convert_unix_to_windows_epoch(unix_timestamp):
    result = convert_unix_to_windows_epoch(unix_timestamp)
    formatted_result = format_value_dt(result, unix_timestamp)
    log_file.write(formatted_result + "\n")
