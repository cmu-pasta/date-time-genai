
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_time_to_seconds_since_midnight(t: time) -> int:
    # Step 1: Extract hour, minute, and second components from the time object.
    # Step 2: Calculate total seconds by converting hours and minutes to seconds
    # and summing them with the existing seconds.
    total_seconds = (t.hour * 3600) + (t.minute * 60) + t.second
    
    # Step 3: Return the calculated total seconds as an integer.
    return total_seconds

# Entry point: convert_time_to_seconds_since_midnight(t: time) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_40_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_seconds_since_midnight(t):
    result = convert_time_to_seconds_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
