
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def timestamp_to_filetime(timestamp: float) -> int:
    """
    Converts a POSIX timestamp to a Windows FILETIME value.
    
    Args:
        timestamp (float): The POSIX timestamp (seconds since 1970-01-01T00:00:00Z).
    
    Returns:
        int: The corresponding Windows FILETIME value (number of 100-nanosecond intervals since 1601-01-01T00:00:00Z).
    """
    # Step 1: Define the number of seconds between 1601-01-01 and 1970-01-01
    EPOCH_DIFFERENCE_SECONDS = 11644473600

    # Step 2: Add the offset to convert to seconds since 1601-01-01
    filetime_seconds = timestamp + EPOCH_DIFFERENCE_SECONDS
    
    # Step 3: Convert to 100-nanosecond intervals
    filetime_intervals = int(filetime_seconds * 10_000_000)
    
    # Step 4: Return the FILETIME integer value
    return filetime_intervals

# Entry point: timestamp_to_filetime(timestamp: float) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_65txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_timestamp_to_filetime(timestamp):
    result = timestamp_to_filetime(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
