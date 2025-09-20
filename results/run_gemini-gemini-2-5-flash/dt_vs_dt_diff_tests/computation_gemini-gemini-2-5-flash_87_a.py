
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Calculate the timedelta between the two datetime objects.
    # The datetime objects inherently store time with microsecond precision.
    # The difference will be a timedelta object.
    time_difference = dt2 - dt1
    
    # Step 2: Get the total number of seconds from the timedelta as a float.
    # This correctly accounts for days, seconds, and microseconds.
    total_seconds = time_difference.total_seconds()
    
    # Step 3: Convert total seconds to nanoseconds.
    # There are 1,000,000,000 nanoseconds in one second.
    # Note: Since Python's datetime only supports microsecond precision,
    # the resulting nanosecond value will always be a multiple of 1000.
    total_nanoseconds = total_seconds * 1_000_000_000
    
    # Step 4: Return the absolute difference as an integer.
    return int(abs(total_nanoseconds))

# Entry point: calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_87_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_difference(dt1, dt2):
    result = calculate_nanoseconds_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
