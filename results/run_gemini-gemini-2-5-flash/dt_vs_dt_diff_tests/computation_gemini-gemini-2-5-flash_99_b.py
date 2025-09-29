
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def calculate_decimal_time(t: time) -> float:
    # Step 1: Calculate the total number of seconds represented by the time object since midnight.
    # Convert hours, minutes, seconds, and microseconds to seconds.
    total_seconds_for_time = (
        t.hour * 3600 +
        t.minute * 60 +
        t.second +
        t.microsecond / 1_000_000
    )
    
    # Step 2: Calculate the total number of seconds in a full day.
    # 24 hours * 60 minutes/hour * 60 seconds/minute = 86400 seconds
    total_seconds_in_day = 24 * 60 * 60
    
    # Step 3: Compute the decimal time representation.
    # This is the fraction of the day that has passed.
    decimal_time = total_seconds_for_time / total_seconds_in_day
    
    # Step 4: Return the result as a float.
    return decimal_time

# Entry point: calculate_decimal_time(t: time) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_99_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_calculate_decimal_time(t):
    result = calculate_decimal_time(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
