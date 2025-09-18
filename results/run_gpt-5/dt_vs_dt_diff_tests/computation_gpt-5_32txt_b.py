
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    """
    Compute the exact midpoint datetime between two given datetime values.
    
    Parameters:
    - dt1: datetime
    - dt2: datetime
    
    Returns:
    - datetime: The datetime exactly halfway between dt1 and dt2.
    """
    # Calculate half of the absolute difference between the two datetimes
    half_delta: timedelta = abs(dt2 - dt1) / 2

    # Use the earlier datetime as the base and add the half-difference
    base: datetime = dt1 if dt1 <= dt2 else dt2
    return base + half_delta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_32txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_midpoint_datetime(dt1, dt2):
    result = midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
