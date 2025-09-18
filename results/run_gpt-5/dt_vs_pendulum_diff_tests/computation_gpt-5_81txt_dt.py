
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def calculate_milliseconds(duration: timedelta) -> float:
    """
    Calculate the number of milliseconds in a given time duration.

    Args:
        duration (timedelta): The time duration to convert.

    Returns:
        float: The total number of milliseconds in the duration.
    """
    # Convert duration to total seconds and then to milliseconds
    return duration.total_seconds() * 1000.0

# Entry point: calculate_milliseconds(duration: timedelta) -> float

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_81txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_calculate_milliseconds(duration):
    result = calculate_milliseconds(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
