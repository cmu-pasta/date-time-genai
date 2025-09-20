
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12_to_24_hour(twelve_hour_time: time, is_pm: bool) -> time:
    # Step 1: Extract hour, minute, second, and microsecond from the input time
    hour = twelve_hour_time.hour
    minute = twelve_hour_time.minute
    second = twelve_hour_time.second
    microsecond = twelve_hour_time.microsecond
    
    # Step 2: Convert 12-hour format to 24-hour format
    if is_pm:
        # PM case: add 12 to hours 1-11, keep 12 as is
        if hour != 12:
            hour += 12
    else:
        # AM case: keep hours 1-11 as is, convert 12 to 0
        if hour == 12:
            hour = 0
    
    # Step 3: Create and return the 24-hour time object
    return time(hour, minute, second, microsecond)

# Entry point: convert_12_to_24_hour(twelve_hour_time: time, is_pm: bool) -> time

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_22_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12_to_24_hour(twelve_hour_time, is_pm):
    result = convert_12_to_24_hour(twelve_hour_time, is_pm)
    formatted_result = format_value_dt(result, twelve_hour_time, is_pm)
    log_file.write(formatted_result + "\n")
