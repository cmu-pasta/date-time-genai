
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def duration_to_hours(duration: timedelta) -> float:
    """
    Convert a time duration to total hours as a decimal number.

    Args:
        duration: A datetime.timedelta representing the duration.

    Returns:
        A float representing the total hours (including fractional part).
    """
    return duration.total_seconds() / 3600.0

# Entry point: duration_to_hours(duration: timedelta) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_88_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_duration_to_hours(duration):
    result = duration_to_hours(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
