
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_duration_milliseconds(ts1: datetime, ts2: datetime) -> int:
    """
    Calculate the duration between two timestamps in milliseconds.

    Args:
        ts1: The first timestamp as a datetime object.
        ts2: The second timestamp as a datetime object.

    Returns:
        An integer representing the absolute duration between ts1 and ts2 in milliseconds.
    """
    # Step 1: Compute the absolute difference as a timedelta
    delta: timedelta = abs(ts2 - ts1)

    # Step 2: Convert timedelta to milliseconds (integer)
    # Using floor division by 1 millisecond to get an integer count of milliseconds
    milliseconds: int = delta // timedelta(milliseconds=1)

    # Step 3: Return the result
    return milliseconds

# Entry point: calculate_duration_milliseconds(ts1: datetime, ts2: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_36txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_duration_milliseconds(ts1, ts2):
    result = calculate_duration_milliseconds(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
