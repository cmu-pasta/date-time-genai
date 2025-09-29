
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Calculate the total time difference between the two datetimes.
    # The order of subtraction determines the sign of the timedelta,
    # but the subsequent addition will correctly find the midpoint regardless.
    total_difference: timedelta = dt2 - dt1
    
    # Step 2: Calculate half of the total time difference.
    half_difference: timedelta = total_difference / 2
    
    # Step 3: Add this half difference to the first datetime to find the midpoint.
    midpoint_dt: datetime = dt1 + half_difference
    
    # Step 4: Return the calculated midpoint datetime.
    return midpoint_dt

# Entry point: find_midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_26_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_midpoint_datetime(dt1, dt2):
    result = find_midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
