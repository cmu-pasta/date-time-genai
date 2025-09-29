
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def time_to_decimal_hours(t: time) -> float:
    # Calculate decimal hours: hours + minutes/60 + seconds/3600 + microseconds/3_600_000_000
    return (
        t.hour
        + t.minute / 60.0
        + t.second / 3600.0
        + t.microsecond / 3_600_000_000.0
    )

# Entry point: time_to_decimal_hours(t: time) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_99_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_time_to_decimal_hours(t):
    result = time_to_decimal_hours(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
