
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_time_difference_with_timezones(dt1: datetime, dt2: datetime) -> timedelta:
    """
    Calculate the time difference between two datetime objects accounting for different time zones.
    
    Args:
        dt1: First datetime object (should be timezone-aware)
        dt2: Second datetime object (should be timezone-aware)
    
    Returns:
        timedelta: The time difference between dt2 and dt1
    """
    # If either datetime is timezone-naive, we assume UTC
    if dt1.tzinfo is None:
        dt1 = dt1.replace(tzinfo=ZoneInfo("UTC"))
    if dt2.tzinfo is None:
        dt2 = dt2.replace(tzinfo=ZoneInfo("UTC"))
    
    # Calculate the difference - Python automatically handles timezone conversion
    difference = dt2 - dt1
    
    return difference

# Entry point: calculate_time_difference_with_timezones(dt1: datetime, dt2: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_69txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_time_difference_with_timezones(dt1, dt2):
    result = calculate_time_difference_with_timezones(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
