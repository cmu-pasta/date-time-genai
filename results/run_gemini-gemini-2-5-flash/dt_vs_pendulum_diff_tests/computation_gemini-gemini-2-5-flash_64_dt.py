
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_time_to_minutes_since_midnight(input_time: time) -> int:
    # Step 1: Extract hours and minutes from the time object
    hours = input_time.hour
    minutes = input_time.minute
    
    # Step 2: Calculate the total minutes since midnight
    total_minutes = (hours * 60) + minutes
    
    # Step 3: Return the result as an integer
    return total_minutes

# Entry point: convert_time_to_minutes_since_midnight(input_time: time) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_64_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_minutes_since_midnight(input_time):
    result = convert_time_to_minutes_since_midnight(input_time)
    formatted_result = format_value_dt(result, input_time)
    log_file.write(formatted_result + "\n")
