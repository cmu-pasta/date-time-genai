
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def decimal_time_of_day(t: time) -> float:
    """
    Calculate the decimal time representation (in hours) for a given time of day.
    For example, 01:30:00 -> 1.5, 12:00:00 -> 12.0

    Args:
        t (time): A time object representing the time of day.

    Returns:
        float: Decimal hours since midnight.
    """
    total_seconds = t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1_000_000
    decimal_hours = total_seconds / 3600.0
    return decimal_hours

# Entry point: decimal_time_of_day(t: time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_99txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_decimal_time_of_day(t):
    result = decimal_time_of_day(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
