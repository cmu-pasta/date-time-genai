
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_exact_time_difference(dt1: datetime, dt2: datetime) -> timedelta:
    """
    Calculates the exact time difference between two timezone-aware datetime objects,
    considering daylight saving time.

    Args:
        dt1: The first timezone-aware datetime object.
        dt2: The second timezone-aware datetime object.

    Returns:
        A timedelta object representing the exact time difference between dt1 and dt2.
        The result is always dt2 - dt1.
    """
    # Ensure both datetime objects are timezone-aware.
    # If they are naive, this function will not correctly account for DST.
    # For this problem, we assume the inputs are already timezone-aware.
    if dt1.tzinfo is None or dt2.tzinfo is None:
        raise ValueError("Input datetime objects must be timezone-aware to correctly account for DST.")

    # Step 1: Calculate the difference between the two timezone-aware datetime objects.
    # The subtraction of two timezone-aware datetimes automatically accounts for
    # any DST changes that occur between them.
    difference = dt2 - dt1
    
    # Step 2: Return the result as a timedelta object.
    return difference

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_1_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_exact_time_difference(dt1, dt2):
    result = calculate_exact_time_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
