
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12h_to_24h(t12: time, is_pm: bool) -> time:
    """
    Convert a 12-hour time to a 24-hour time.

    Inputs:
      - t12: time object whose hour must be in 1..12 (represents 12-hour clock time)
      - is_pm: boolean where True indicates PM, False indicates AM

    Returns:
      - time object in 24-hour format, preserving minutes, seconds, microseconds, tzinfo, and fold.
    """
    # Validate that the provided hour is appropriate for 12-hour format
    if not 1 <= t12.hour <= 12:
        raise ValueError("For 12-hour input, hour must be in the range 1..12.")

    # Map 12 -> 0, 1..11 -> 1..11
    hour_24 = t12.hour % 12

    # Add 12 hours if PM to obtain 24-hour clock
    if is_pm:
        hour_24 += 12

    # Build the 24-hour time while preserving other attributes
    return time(
        hour_24,
        t12.minute,
        t12.second,
        t12.microsecond,
        tzinfo=t12.tzinfo,
        fold=t12.fold,
    )

# Entry point: convert_12h_to_24h(t12: time, is_pm: bool) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_22txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12h_to_24h(t12, is_pm):
    result = convert_12h_to_24h(t12, is_pm)
    formatted_result = format_value_dt(result, t12, is_pm)
    log_file.write(formatted_result + "\n")
