
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    """
    Find the midpoint datetime between two datetimes.

    Rules:
    - If both datetimes are naive, computes midpoint directly and returns a naive datetime.
    - If both are timezone-aware (tzinfo not None), converts both to UTC for computation,
      then returns the midpoint converted to dt1's original timezone.
    - If one is naive and the other is aware, raises ValueError due to ambiguity.
    """
    if (dt1.tzinfo is None) != (dt2.tzinfo is None):
        raise ValueError("Both datetimes must be either naive or timezone-aware.")

    if dt1.tzinfo is not None:
        # Aware datetimes: normalize to UTC for arithmetic
        dt1_utc = dt1.astimezone(timezone.utc)
        dt2_utc = dt2.astimezone(timezone.utc)
        # Compute midpoint in UTC
        half_delta = (dt2_utc - dt1_utc) / 2
        midpoint_utc = dt1_utc + half_delta
        # Convert back to the timezone of dt1
        return midpoint_utc.astimezone(dt1.tzinfo)
    else:
        # Naive datetimes: compute directly
        half_delta = (dt2 - dt1) / 2
        return dt1 + half_delta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_26txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_midpoint_datetime(dt1, dt2):
    result = midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
