
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_time_difference_with_dst(dt1: datetime, dt2: datetime) -> timedelta:
    """
    Calculate the exact time difference between two timestamps considering daylight saving time.
    
    Args:
        dt1: First timezone-aware datetime object
        dt2: Second timezone-aware datetime object
    
    Returns:
        timedelta: The exact time difference between the two timestamps
    """
    # Ensure both datetime objects are timezone-aware
    if dt1.tzinfo is None or dt2.tzinfo is None:
        raise ValueError("Both datetime objects must be timezone-aware to handle DST correctly")
    
    # Calculate the difference - Python automatically handles DST transitions
    time_difference = dt2 - dt1
    
    return time_difference

# Entry point: calculate_time_difference_with_dst(dt1: datetime, dt2: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_1txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_time_difference_with_dst(dt1, dt2):
    result = calculate_time_difference_with_dst(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
