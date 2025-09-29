
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def calculate_minutes_difference(t1: time, t2: time) -> int:
    # Convert a time to total seconds since midnight (including microseconds)
    def seconds_since_midnight(t: time) -> float:
        return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1_000_000

    s1 = seconds_since_midnight(t1)
    s2 = seconds_since_midnight(t2)

    # Absolute difference in seconds
    diff_seconds = abs(s2 - s1)

    # Convert to whole minutes (floor)
    minutes = int(diff_seconds // 60)
    return minutes

# Entry point: calculate_minutes_difference(t1: time, t2: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_33txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_difference(t1, t2):
    result = calculate_minutes_difference(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
