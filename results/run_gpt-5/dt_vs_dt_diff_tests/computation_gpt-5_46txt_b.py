
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_24h_to_12h_ampm(dt: datetime) -> str:
    """
    Convert the time component of a datetime from 24-hour format to 12-hour format with AM/PM.

    Args:
        dt: A datetime object representing the 24-hour time.

    Returns:
        A string representing the time in 12-hour format with AM/PM (e.g., "03:45:00 PM").
    """
    # Step 1: Format using 12-hour clock with AM/PM
    formatted_time = dt.strftime("%I:%M:%S %p")
    return formatted_time

# Entry point: convert_24h_to_12h_ampm(dt: datetime) -> str

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_46txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_24h_to_12h_ampm(dt):
    result = convert_24h_to_12h_ampm(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
