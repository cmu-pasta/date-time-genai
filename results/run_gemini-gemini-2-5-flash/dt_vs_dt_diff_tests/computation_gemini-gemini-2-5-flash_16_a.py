
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_unix_to_datetime(timestamp: float) -> datetime:
    # Step 1: Use datetime.fromtimestamp() to convert the Unix timestamp
    # This method takes a timestamp (seconds since the epoch) and returns a local datetime object.
    human_readable_dt = datetime.fromtimestamp(timestamp)
    
    # Step 2: Return the resulting datetime object
    return human_readable_dt

# Entry point: convert_unix_to_datetime(timestamp: float) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_16_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_convert_unix_to_datetime(timestamp):
    result = convert_unix_to_datetime(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
