
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time, timedelta
def convert_time_to_minutes_since_midnight(t: time) -> int:
    """
    Convert a 24-hour time to the integer number of minutes since midnight.
    
    Parameters:
        t (time): A time object in 24-hour format.
    
    Returns:
        int: Total whole minutes since 00:00.
    """
    # Build a timedelta representing the elapsed time since midnight
    elapsed = timedelta(
        hours=t.hour,
        minutes=t.minute,
        seconds=t.second,
        microseconds=t.microsecond
    )
    
    # Convert elapsed time to whole minutes (floor)
    minutes_since_midnight = elapsed // timedelta(minutes=1)
    
    return int(minutes_since_midnight)

# Entry point: convert_time_to_minutes_since_midnight(t: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_64txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_minutes_since_midnight(t):
    result = convert_time_to_minutes_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
