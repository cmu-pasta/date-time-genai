
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    """
    Compute the midpoint datetime between two datetimes.
    The function supports both naive and timezone-aware datetimes, but both inputs
    must be of the same kind (both naive or both aware).
    """
    # Validate input types
    if not isinstance(dt1, datetime) or not isinstance(dt2, datetime):
        raise TypeError("Both inputs must be datetime instances.")

    # Ensure both are either naive or aware
    if (dt1.tzinfo is None) != (dt2.tzinfo is None):
        raise ValueError("Both datetimes must be either naive or both timezone-aware.")

    # Compute the midpoint
    delta = dt2 - dt1
    midpoint = dt1 + (delta / 2)

    return midpoint

# Entry point: midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_26txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_midpoint_datetime(dt1, dt2):
    result = midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
