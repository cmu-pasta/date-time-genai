
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12h_to_24h(t12: time, is_pm: bool) -> time:
    # Step 1: Extract the hour from the input time
    hour = t12.hour

    # Step 2: Convert based on AM/PM
    if is_pm:
        # For PM, 12 PM stays 12; 1-11 PM becomes 13-23
        hour = 12 if hour == 12 else hour + 12
    else:
        # For AM, 12 AM becomes 0; 1-11 AM stays the same
        hour = 0 if hour == 12 else hour

    # Step 3: Construct and return the 24-hour time, preserving other fields
    return time(
        hour=hour,
        minute=t12.minute,
        second=t12.second,
        microsecond=t12.microsecond,
        tzinfo=t12.tzinfo,
        fold=t12.fold
    )

# Entry point: convert_12h_to_24h(t12: time, is_pm: bool) -> time

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_22_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12h_to_24h(t12, is_pm):
    result = convert_12h_to_24h(t12, is_pm)
    formatted_result = format_value_dt(result, t12, is_pm)
    log_file.write(formatted_result + "\n")
