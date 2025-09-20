
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_exact_time_difference(dt1: datetime, dt2: datetime) -> timedelta:
    # Precondition: Ensure both datetime objects are timezone-aware.
    # If they are not timezone-aware, a ValueError might be raised by the subtraction,
    # or the result might not correctly account for DST.
    if dt1.tzinfo is None or dt2.tzinfo is None:
        raise ValueError("Both input datetime objects must be timezone-aware to calculate exact time difference considering DST.")

    # Step 1: Calculate the difference between the two timezone-aware datetime objects.
    # Python's datetime subtraction automatically handles timezone and DST transitions.
    time_difference = dt2 - dt1
    
    # Step 2: Return the timedelta object representing the exact time difference.
    return time_difference

# Entry point: calculate_exact_time_difference(dt1: datetime, dt2: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_1_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_exact_time_difference(dt1, dt2):
    result = calculate_exact_time_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
