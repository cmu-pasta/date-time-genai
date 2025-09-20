
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_datetime_to_iso8601(dt: datetime) -> str:
    # Step 1: Use the isoformat() method to convert the datetime object to an ISO 8601 string.
    # By default, isoformat() produces a string in YYYY-MM-DDTHH:MM:SS.mmmmmm[+HH:MM] format.
    iso_string = dt.isoformat()
    
    # Step 2: Return the resulting string.
    return iso_string

# Entry point: convert_datetime_to_iso8601(dt: datetime) -> str

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_28_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_datetime_to_iso8601(dt):
    result = convert_datetime_to_iso8601(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
