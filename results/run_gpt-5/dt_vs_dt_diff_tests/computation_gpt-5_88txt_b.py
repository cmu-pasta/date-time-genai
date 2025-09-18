
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def convert_duration_to_hours(duration: timedelta) -> float:
    """
    Convert a time duration to total hours as a decimal number.

    Args:
        duration (timedelta): The time duration to convert.

    Returns:
        float: The total hours represented by the duration as a decimal.
    """
    # Compute total hours by converting total seconds to hours
    total_hours = duration.total_seconds() / 3600.0
    return float(total_hours)

# Entry point: convert_duration_to_hours(duration: timedelta) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_88txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_convert_duration_to_hours(duration):
    result = convert_duration_to_hours(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
