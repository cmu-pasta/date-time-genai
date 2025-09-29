
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def convert_datetime_to_12_hour_time(dt: datetime) -> time:
    # Step 1: Extract the time component from the datetime object.
    # A time object internally stores hours from 0 to 23.
    # The '12-hour format with AM/PM' is a display format,
    # which is usually applied when converting the time object to a string.
    # Since string output is disallowed by constraint 'g',
    # we return the standard 'time' object.
    # The caller can then use strftime to display it in 12-hour format with AM/PM.
    return dt.timetz() if dt.tzinfo is not None else dt.time()

# Entry point: convert_datetime_to_12_hour_time(dt: datetime) -> time

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_46_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_datetime_to_12_hour_time(dt):
    result = convert_datetime_to_12_hour_time(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
