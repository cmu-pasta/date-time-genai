
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def round_time_up_to_next_quarter(input_time: time) -> time:
    """
    Rounds a given time up to the next quarter hour.
    Returns a time object with minute one of {0, 15, 30, 45}, and zero seconds and microseconds.
    If the input is already exactly on a quarter hour, returns the same time.
    """
    # Step 1: Extract hour, minute, second, microsecond
    hour = input_time.hour
    minute = input_time.minute
    second = input_time.second
    microsecond = input_time.microsecond
    tzinfo = input_time.tzinfo
    
    # Step 2: Check if already on a quarter-hour
    if minute % 15 == 0 and second == 0 and microsecond == 0:
        return input_time

    # Step 3: Calculate total minutes and advance to next quarter
    # If there are any seconds or microseconds, consider as the next minute
    if second != 0 or microsecond != 0:
        minute += 1
        if minute == 60:
            hour += 1
            minute = 0
    
    # Find how many minutes past the last quarter
    remainder = minute % 15
    if remainder != 0:
        increment = 15 - remainder
        minute += increment
        if minute >= 60:
            minute -= 60
            hour += 1
    
    # Handle wrap-around at midnight (24:00 should become 00:00)
    if hour >= 24:
        hour = 0
    
    # Step 4: Return new time object rounded up
    return time(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=tzinfo)

# Entry point: round_time_up_to_next_quarter(input_time: time) -> time

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_23txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_round_time_up_to_next_quarter(input_time):
    result = round_time_up_to_next_quarter(input_time)
    formatted_result = format_value_dt(result, input_time)
    log_file.write(formatted_result + "\n")
