
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
# Define epoch constants (UTC)
UNIX_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
WINDOWS_FILETIME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

def unix_to_windows_filetime(unix_seconds: float) -> int:
    """
    Convert a Unix timestamp (seconds since 1970-01-01 UTC) to Windows FILETIME
    (number of 100-nanosecond intervals since 1601-01-01 UTC).
    
    Args:
        unix_seconds: Seconds since Unix epoch. Can be negative or fractional.
    Returns:
        Integer count of 100-nanosecond intervals since Windows FILETIME epoch.
    """
    # Convert Unix seconds to an absolute UTC datetime
    dt = UNIX_EPOCH + timedelta(seconds=unix_seconds)
    # Find the difference from Windows epoch
    delta = dt - WINDOWS_FILETIME_EPOCH
    # FILETIME is in 100-nanosecond ticks
    return int(delta.total_seconds() * 10_000_000)

def windows_filetime_to_unix_seconds(filetime: int) -> float:
    """
    Convert a Windows FILETIME integer to a Unix timestamp in seconds.
    
    Args:
        filetime: Integer number of 100-nanosecond intervals since 1601-01-01 UTC.
    Returns:
        Seconds since Unix epoch as a float.
    """
    # Convert FILETIME ticks to a datetime
    seconds = filetime / 10_000_000.0
    dt = WINDOWS_FILETIME_EPOCH + timedelta(seconds=seconds)
    # Compute Unix seconds
    return (dt - UNIX_EPOCH).total_seconds()

# Entry point: unix_to_windows_filetime(unix_seconds: float) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_58txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_unix_to_windows_filetime(unix_seconds):
    result = unix_to_windows_filetime(unix_seconds)
    formatted_result = format_value_dt(result, unix_seconds)
    log_file.write(formatted_result + "\n")
