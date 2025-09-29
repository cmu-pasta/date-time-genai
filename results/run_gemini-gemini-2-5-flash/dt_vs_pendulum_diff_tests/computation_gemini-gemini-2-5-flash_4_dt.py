
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def convert_timezone(timestamp: datetime, target_timezone: ZoneInfo) -> datetime:
    """
    Converts a timezone-aware datetime object from its current timezone to a specified target timezone.

    Args:
        timestamp: A timezone-aware datetime object representing the timestamp in its source timezone.
                   The datetime object must have a tzinfo attribute set.
        target_timezone: A ZoneInfo object representing the desired target timezone.

    Returns:
        A new datetime object representing the same point in time, but adjusted to the target timezone.
    """
    if timestamp.tzinfo is None:
        raise ValueError("Input 'timestamp' must be timezone-aware.")
    
    # Step 1: Use astimezone() to convert the datetime object to the target timezone.
    # The astimezone() method correctly handles the conversion from the current timezone
    # of the 'timestamp' to the 'target_timezone'.
    converted_timestamp = timestamp.astimezone(target_timezone)
    
    # Step 2: Return the new timezone-aware datetime object.
    return converted_timestamp

# Entry point: convert_timezone(timestamp: datetime, target_timezone: ZoneInfo) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_4_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_convert_timezone(timestamp, target_timezone):
    result = convert_timezone(timestamp, target_timezone)
    formatted_result = format_value_dt(result, timestamp, target_timezone)
    log_file.write(formatted_result + "\n")
