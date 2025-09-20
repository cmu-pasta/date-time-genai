
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def time_difference_hours(t1: time, t2: time) -> float:
    # Convert each time to total seconds since midnight, including microseconds
    seconds1 = t1.hour * 3600 + t1.minute * 60 + t1.second + t1.microsecond / 1_000_000
    seconds2 = t2.hour * 3600 + t2.minute * 60 + t2.second + t2.microsecond / 1_000_000

    # Absolute difference in hours
    return abs(seconds2 - seconds1) / 3600.0

# Entry point: time_difference_hours(t1: time, t2: time) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_18_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_time_difference_hours(t1, t2):
    result = time_difference_hours(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
