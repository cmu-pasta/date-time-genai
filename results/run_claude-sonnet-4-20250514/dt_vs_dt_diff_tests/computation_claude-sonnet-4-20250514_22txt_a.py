
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12_to_24_hour(time_12h: time, is_pm: bool) -> time:
    """
    Convert 12-hour time format to 24-hour time format.
    
    Args:
        time_12h: A time object representing the time in 12-hour format
        is_pm: Boolean indicating if the time is PM (True) or AM (False)
    
    Returns:
        A time object in 24-hour format
    """
    hour = time_12h.hour
    minute = time_12h.minute
    second = time_12h.second
    microsecond = time_12h.microsecond
    
    # Handle conversion logic
    if is_pm:
        if hour == 12:
            # 12 PM stays as 12 (noon)
            new_hour = 12
        else:
            # Add 12 to convert PM hours (1-11 PM becomes 13-23)
            new_hour = hour + 12
    else:
        if hour == 12:
            # 12 AM becomes 0 (midnight)
            new_hour = 0
        else:
            # AM hours (1-11) stay the same
            new_hour = hour
    
    # Return the new time object in 24-hour format
    return time(new_hour, minute, second, microsecond)

# Entry point: convert_12_to_24_hour(time_12h: time, is_pm: bool) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_22txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12_to_24_hour(time_12h, is_pm):
    result = convert_12_to_24_hour(time_12h, is_pm)
    formatted_result = format_value_dt(result, time_12h, is_pm)
    log_file.write(formatted_result + "\n")
