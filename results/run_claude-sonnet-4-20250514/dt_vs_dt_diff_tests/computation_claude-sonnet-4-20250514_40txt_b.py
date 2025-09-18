
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_time_to_seconds_since_midnight(t: time) -> float:
    # Step 1: Calculate total seconds since midnight
    # Convert hours to seconds (1 hour = 3600 seconds)
    hours_in_seconds = t.hour * 3600
    
    # Convert minutes to seconds (1 minute = 60 seconds) 
    minutes_in_seconds = t.minute * 60
    
    # Get seconds directly
    seconds = t.second
    
    # Convert microseconds to seconds (1 second = 1,000,000 microseconds)
    microseconds_in_seconds = t.microsecond / 1000000
    
    # Step 2: Sum all components to get total seconds since midnight
    total_seconds = hours_in_seconds + minutes_in_seconds + seconds + microseconds_in_seconds
    
    # Step 3: Return the result as a float
    return total_seconds

# Entry point: convert_time_to_seconds_since_midnight(t: time) -> float

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_40txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_seconds_since_midnight(t):
    result = convert_time_to_seconds_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
