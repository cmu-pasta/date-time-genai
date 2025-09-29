
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def convert_timedelta_to_total_hours(duration: timedelta) -> float:
    # Step 1: Get the total number of seconds in the timedelta
    total_seconds = duration.total_seconds()
    
    # Step 2: Convert total seconds to total hours (decimal)
    # There are 3600 seconds in an hour
    total_hours = total_seconds / 3600.0
    
    # Step 3: Return the result as a float
    return total_hours

# Entry point: convert_timedelta_to_total_hours(duration: timedelta) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_88_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_convert_timedelta_to_total_hours(duration):
    result = convert_timedelta_to_total_hours(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
