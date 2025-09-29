
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def convert_timestamp_epoch(timestamp: float, from_unix_to_windows: bool) -> float:
    # Define epoch starting points
    unix_epoch = datetime(1970, 1, 1)
    windows_epoch = datetime(1601, 1, 1)
    
    if from_unix_to_windows:
        # Convert from Unix timestamp to datetime (UTC)
        dt = datetime.utcfromtimestamp(timestamp)
        # Calculate seconds since Windows epoch
        delta = dt - windows_epoch
        return delta.total_seconds()
    else:
        # Convert from Windows timestamp to datetime
        dt = windows_epoch + timedelta(seconds=timestamp)
        # Calculate seconds since Unix epoch
        delta = dt - unix_epoch
        return delta.total_seconds()

# Entry point: convert_timestamp_epoch(timestamp: float, from_unix_to_windows: bool) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_58_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), bool_strategy())
def test_convert_timestamp_epoch(timestamp, from_unix_to_windows):
    result = convert_timestamp_epoch(timestamp, from_unix_to_windows)
    formatted_result = format_value_dt(result, timestamp, from_unix_to_windows)
    log_file.write(formatted_result + "\n")
