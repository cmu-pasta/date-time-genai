
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def convert_12h_to_24h(t12: time, is_pm: bool) -> time:
    # Validate that the provided time follows 12-hour format (hour must be 1..12)
    if t12.hour < 1 or t12.hour > 12:
        raise ValueError("For 12-hour input, hour must be in the range 1..12.")
    
    hour = t12.hour
    # Conversion rules:
    # - For AM: 12 AM -> 0, 1..11 AM -> 1..11
    # - For PM: 12 PM -> 12, 1..11 PM -> 13..23
    if is_pm:
        hour_24 = 12 if hour == 12 else hour + 12
    else:
        hour_24 = 0 if hour == 12 else hour

    # Preserve minute, second, microsecond, tzinfo, and fold
    return t12.replace(hour=hour_24)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_22_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12h_to_24h(t12, is_pm):
    result = convert_12h_to_24h(t12, is_pm)
    formatted_result = format_value_dt(result, t12, is_pm)
    log_file.write(formatted_result + "\n")
