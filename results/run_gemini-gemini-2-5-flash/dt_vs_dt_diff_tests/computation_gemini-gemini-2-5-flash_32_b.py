
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_middle_date(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Calculate the total time difference between the two dates
    # The order of subtraction (dt2 - dt1 or dt1 - dt2) doesn't strictly matter
    # if we add half the difference to the earlier date, or subtract from the later.
    # A simpler approach is to always add (dt2 - dt1) / 2 to dt1.
    total_difference: timedelta = dt2 - dt1
    
    # Step 2: Calculate half of the total difference
    half_difference: timedelta = total_difference / 2
    
    # Step 3: Add the half difference to the first date to find the middle date
    middle_date: datetime = dt1 + half_difference
    
    # Step 4: Return the computed middle date
    return middle_date

# Entry point: find_middle_date(dt1: datetime, dt2: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_32_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_middle_date(dt1, dt2):
    result = find_middle_date(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
