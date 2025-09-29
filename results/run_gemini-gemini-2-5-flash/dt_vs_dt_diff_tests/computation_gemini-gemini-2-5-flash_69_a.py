
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo # Requires Python 3.9+ for ZoneInfo
def calculate_timezone_aware_difference(dt1: datetime, dt2: datetime) -> timedelta:
    """
    Calculates the time difference between two timezone-aware datetime objects.

    Args:
        dt1: The first datetime object. Must be timezone-aware.
        dt2: The second datetime object. Must be timezone-aware.

    Returns:
        A timedelta object representing the difference (dt2 - dt1).
    """
    # It is crucial that both dt1 and dt2 are timezone-aware for this
    # calculation to correctly account for different time zones.
    # If they are naive, this function will still work but will not
    # "account" for time zones beyond simple clock time difference.
    # If one is naive and the other aware, a TypeError will be raised.

    # Perform the subtraction. Python's datetime subtraction correctly
    # handles timezone-aware objects, giving the actual elapsed time.
    time_difference = dt2 - dt1
    
    return time_difference

# Entry point: calculate_timezone_aware_difference(dt1: datetime, dt2: datetime) -> timedelta

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_69_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_timezone_aware_difference(dt1, dt2):
    result = calculate_timezone_aware_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
