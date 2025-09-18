
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> time:
    """
    Convert 12-hour time format to 24-hour time format.
    
    Args:
        hour: Hour in 12-hour format (1-12)
        minute: Minutes (0-59)
        second: Seconds (0-59)
        is_pm: True for PM, False for AM
    
    Returns:
        time object in 24-hour format
    """
    # Convert hour from 12-hour to 24-hour format
    if is_pm:
        # PM case: 12 PM stays 12, 1-11 PM becomes 13-23
        if hour == 12:
            hour_24 = 12
        else:
            hour_24 = hour + 12
    else:
        # AM case: 12 AM becomes 0, 1-11 AM stays 1-11
        if hour == 12:
            hour_24 = 0
        else:
            hour_24 = hour
    
    # Create and return the time object
    return time(hour_24, minute, second)

# Entry point: convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_22txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), bool_strategy())
def test_convert_12_to_24_hour(hour, minute, second, is_pm):
    result = convert_12_to_24_hour(hour, minute, second, is_pm)
    formatted_result = format_value_dt(result, hour, minute, second, is_pm)
    log_file.write(formatted_result + "\n")
