
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_seconds_difference(ts1: datetime, ts2: datetime) -> float:
    """
    Calculate the absolute number of seconds between two datetime timestamps.

    Args:
        ts1: The first datetime timestamp.
        ts2: The second datetime timestamp.

    Returns:
        A float representing the absolute number of seconds between ts1 and ts2.
    """
    # Ensure both datetimes are either naive or both timezone-aware
    if (ts1.tzinfo is None) != (ts2.tzinfo is None):
        raise ValueError("Both datetimes must be either naive or both timezone-aware.")

    # Compute the time difference
    delta = ts2 - ts1

    # Return the absolute number of seconds (including fractions)
    return abs(delta.total_seconds())

# Entry point: calculate_seconds_difference(ts1: datetime, ts2: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_9txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_seconds_difference(ts1, ts2):
    result = calculate_seconds_difference(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
