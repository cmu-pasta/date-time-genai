
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def convert_timestamp_to_windows_epoch(unix_timestamp: float) -> int:
    """
    Converts a Unix timestamp (seconds since 1970-01-01 00:00:00 UTC)
    to a Windows FileTime (100-nanosecond intervals since 1601-01-01 00:00:00 UTC).

    Args:
        unix_timestamp: A float representing seconds since the Unix epoch.

    Returns:
        An integer representing 100-nanosecond intervals since the Windows epoch.
    """
    # Step 1: Define the Unix epoch (source epoch)
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

    # Step 2: Define the Windows epoch (target epoch)
    windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)

    # Step 3: Convert the input Unix timestamp to a datetime object
    # This datetime object represents the exact point in time universally.
    # We add the timedelta of the unix_timestamp to the unix_epoch.
    universal_dt = unix_epoch + timedelta(seconds=unix_timestamp)

    # Step 4: Calculate the timedelta from the Windows epoch to the universal datetime
    time_since_windows_epoch = universal_dt - windows_epoch

    # Step 5: Convert the timedelta to 100-nanosecond intervals
    # There are 10,000,000 (10^7) 100-nanosecond intervals in one second.
    # We use total_seconds() to get the full duration as a float.
    total_hundred_ns = int(time_since_windows_epoch.total_seconds() * 10_000_000)

    return total_hundred_ns

# Entry point: convert_timestamp_to_windows_epoch(unix_timestamp: float) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_58_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_convert_timestamp_to_windows_epoch(unix_timestamp):
    result = convert_timestamp_to_windows_epoch(unix_timestamp)
    formatted_result = format_value_dt(result, unix_timestamp)
    log_file.write(formatted_result + "\n")
