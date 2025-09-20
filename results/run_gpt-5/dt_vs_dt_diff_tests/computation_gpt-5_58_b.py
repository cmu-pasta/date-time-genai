
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def convert_unix_to_windows_filetime(unix_seconds: float) -> int:
    # Step 1: Define epochs in UTC
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    
    # Step 2: Build datetime from Unix seconds
    unix_dt = unix_epoch + timedelta(seconds=unix_seconds)
    
    # Step 3: Compute timedelta relative to Windows epoch
    delta = unix_dt - windows_epoch
    
    # Step 4: Convert to Windows FILETIME ticks (100-nanosecond units)
    ticks = int(delta.total_seconds() * 10_000_000)
    return ticks

# Entry point: convert_unix_to_windows_filetime(unix_seconds: float) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_58_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_convert_unix_to_windows_filetime(unix_seconds):
    result = convert_unix_to_windows_filetime(unix_seconds)
    formatted_result = format_value_dt(result, unix_seconds)
    log_file.write(formatted_result + "\n")
