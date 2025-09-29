
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def _time_to_seconds_since_midnight(t: time) -> float:
    """
    Convert a time object to fractional seconds since midnight.
    """
    return (
        t.hour * 3600
        + t.minute * 60
        + t.second
        + t.microsecond / 1_000_000
    )

def calculate_time_difference_hours(t1: time, t2: time) -> float:
    """
    Calculate the absolute time difference between two times on the same day,
    expressed in hours as a float.

    Parameters:
    - t1: time
    - t2: time

    Returns:
    - float: absolute difference in hours
    """
    seconds_diff = abs(_time_to_seconds_since_midnight(t2) - _time_to_seconds_since_midnight(t1))
    return seconds_diff / 3600.0

# Entry point: calculate_time_difference_hours(t1: time, t2: time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_18txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_time_difference_hours(t1, t2):
    result = calculate_time_difference_hours(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
